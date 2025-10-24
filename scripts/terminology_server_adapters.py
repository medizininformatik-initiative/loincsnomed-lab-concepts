#!/usr/bin/env python3
"""
Terminology Server Adapters for ECL Query Execution
====================================================
Supports multiple terminology server backends:
- LOINCSNOMED Snowstorm instance (http://browser.loincsnomed.org)
- OntoServer instance (configurable endpoint)

This adapter pattern allows seamless switching between servers without
changing the core query logic.
"""

import time
import os
from pathlib import Path
import getpass

try:
    from dotenv import load_dotenv
    # Load .env from parent directory (project root)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("Warning: python-dotenv not installed, environment variables must be set manually")

import requests

try:
    from requests_pkcs12 import Pkcs12Adapter
    HAS_PKCS12 = True

    # Enable legacy PKCS12 support for older certificates
    try:
        from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
        from cryptography.hazmat.backends import default_backend
        # Just importing TripleDES enables legacy support
    except ImportError:
        # Legacy support not available in this version
        pass
except ImportError:
    HAS_PKCS12 = False
    print("Warning: requests-pkcs12 not installed, mTLS authentication will not work")


class TerminologyServerAdapter(object):
    """Base adapter interface for terminology servers."""

    def execute_ecl_query(self, ecl_expression, limit=1000):
        """
        Execute ECL query against terminology server.

        Args:
            ecl_expression: ECL query string
            limit: Max results

        Returns:
            dict with 'items', 'total', 'execution_time'
        """
        raise NotImplementedError("Subclasses must implement execute_ecl_query")

    def get_concept_details(self, concept_id):
        """
        Get full concept details including descriptions.

        Args:
            concept_id: SNOMED concept ID

        Returns:
            dict with 'concept_id', 'fsn', 'pt'
        """
        raise NotImplementedError("Subclasses must implement get_concept_details")


class LOINCSNOMEDSnowstormAdapter(TerminologyServerAdapter):
    """Adapter for LOINCSNOMED public Snowstorm instance."""

    def __init__(self, api_base=None, branch=None):
        """
        Initialize LOINCSNOMED adapter.

        Args:
            api_base: Base URL (default: http://browser.loincsnomed.org/snowstorm/snomed-ct)
            branch: Branch path (default: MAIN/LOINC/2025-09-21)
        """
        self.api_base = api_base or "http://browser.loincsnomed.org/snowstorm/snomed-ct"
        self.branch = branch or "MAIN/LOINC/2025-09-21"

    def execute_ecl_query(self, ecl_expression, limit=1000):
        """Execute ECL query against LOINCSNOMED Snowstorm."""
        url = "{}/{}/concepts".format(self.api_base, self.branch)
        params = {
            "ecl": ecl_expression,
            "limit": limit,
            "activeFilter": "true"
        }

        start_time = time.time()

        try:
            response = requests.get(url, params=params)
            execution_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                result['execution_time'] = execution_time
                return result
            else:
                print("  Error: {} - {}".format(response.status_code, response.text))
                return {"items": [], "total": 0, "execution_time": execution_time}
        except Exception as e:
            print("  Error: {}".format(str(e)))
            return {"items": [], "total": 0, "execution_time": time.time() - start_time}

    def get_concept_details(self, concept_id):
        """Get concept details from LOINCSNOMED Snowstorm."""
        url = "{}/{}/concepts/{}".format(self.api_base, self.branch, concept_id)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Extract FSN
                fsn = None
                for desc in data.get('descriptions', []):
                    if desc.get('type', {}).get('conceptId') == '900000000000003001':  # FSN type
                        fsn = desc.get('term')
                        break

                return {
                    'concept_id': concept_id,
                    'fsn': fsn or data.get('fsn', {}).get('term', 'Unknown'),
                    'pt': data.get('pt', {}).get('term', 'Unknown')
                }
            else:
                return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}
        except Exception as e:
            print("    Warning: Could not get details for {}: {}".format(concept_id, str(e)))
            return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}


class OntoServerAdapter(TerminologyServerAdapter):
    """Adapter for OntoServer FHIR terminology server."""

    def __init__(self, base_url, code_system_url=None, version_url=None, use_post=False,
                 cert_path=None, cert_password=None):
        """
        Initialize OntoServer adapter.

        Args:
            base_url: OntoServer base URL (e.g., https://ontoserver.mii-termserv.de/fhir)
            code_system_url: SNOMED CT code system URL
                (default: http://snomed.info/sct)
            version_url: Version URL for SNOMED CT
                (default: http://snomed.info/sct/11010000107/version/20250921)
            use_post: If True, use POST with ValueSet body; if False, use GET with fhir_vs parameter
            cert_path: Path to .p12 client certificate file for mTLS authentication
            cert_password: Password for the .p12 certificate (can be None if no password)
        """
        self.base_url = base_url.rstrip('/')
        self.code_system_url = code_system_url or "http://snomed.info/sct"
        self.version_url = version_url or "http://snomed.info/sct/11010000107/version/20250921"
        self.use_post = use_post

        # Load certificate configuration from environment if not provided
        if cert_path is None:
            auth_path = os.getenv('auth_path', '')
            auth_file = os.getenv('auth_file', '')
            if auth_path and auth_file:
                # Remove quotes if present
                auth_file = auth_file.strip('"\'')
                # Use os.path.join for cross-platform compatibility
                cert_path = os.path.join(auth_path, auth_file)

        if cert_password is None:
            cert_password = os.getenv('auth_pw')
            # Convert empty string or 'None' to actual None
            if not cert_password or cert_password in ('None', 'none'):
                cert_password = None

        self.cert_path = cert_path
        self.cert_password = cert_password

    def _get_session(self):
        """
        Create a requests session with certificate authentication.
        Returns a session configured for mTLS if certificate is available.
        """
        session = requests.Session()

        if not HAS_PKCS12:
            print("  Warning: requests-pkcs12 not available, using standard session (authentication will fail)")
            return session

        if self.cert_path and os.path.exists(self.cert_path):
            try:
                # Try with legacy PKCS12 loader first
                try:
                    from cryptography.hazmat.primitives.serialization import pkcs12
                    from cryptography.hazmat.backends import default_backend
                    import ssl
                    import tempfile

                    # Read PKCS12 file with legacy backend support
                    with open(self.cert_path, 'rb') as f:
                        p12_data = f.read()

                    # Load with legacy support - password as bytes or None
                    password_bytes = None
                    if self.cert_password:
                        password_bytes = self.cert_password.encode() if isinstance(self.cert_password, str) else self.cert_password

                    # Load the PKCS12 with unsafe_skip_verification for legacy certs
                    private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
                        p12_data,
                        password_bytes,
                        backend=default_backend()
                    )

                    # Create PEM files temporarily
                    from cryptography.hazmat.primitives import serialization

                    cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
                    key_pem = private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    )

                    # Write to temp files
                    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
                    key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')

                    cert_file.write(cert_pem)
                    cert_file.close()
                    key_file.write(key_pem)
                    key_file.close()

                    # Use standard requests with PEM files
                    session.cert = (cert_file.name, key_file.name)
                    return session

                except Exception as e_legacy:
                    # If legacy approach fails, try Pkcs12Adapter
                    adapter = Pkcs12Adapter(
                        pkcs12_filename=self.cert_path,
                        pkcs12_password=self.cert_password
                    )
                    session.mount('https://', adapter)
                    return session
            except Exception as e:
                print("  Warning: Could not load certificate: {}".format(str(e)))
                return session
        else:
            if self.cert_path:
                print("  Warning: Certificate file not found: {}".format(self.cert_path))
            return session

    def execute_ecl_query(self, ecl_expression, limit=1000):
        """
        Execute ECL query against OntoServer using $expand operation.

        Supports two methods:
        - GET with fhir_vs parameter (default)
        - POST with ValueSet body (if use_post=True)
        """
        import urllib.parse

        url = "{}/ValueSet/$expand".format(self.base_url)
        start_time = time.time()

        try:
            session = self._get_session()

            if self.use_post:
                # Method 2: POST with ValueSet body
                valueset_body = {
                    "resourceType": "ValueSet",
                    "compose": {
                        "include": [
                            {
                                "system": self.code_system_url,
                                "version": self.version_url,
                                "filter": [
                                    {
                                        "property": "constraint",
                                        "op": "=",
                                        "value": ecl_expression
                                    }
                                ]
                            }
                        ]
                    }
                }

                headers = {"Content-Type": "application/json"}
                params = {"count": limit}

                response = session.post(url, json=valueset_body, params=params, headers=headers)
            else:
                # Method 1: GET with fhir_vs parameter
                # The fhir_vs is part of the url parameter value, not a separate parameter
                ecl_param = "ecl/{}".format(urllib.parse.quote(ecl_expression, safe=''))
                url_with_fhir_vs = "{}?fhir_vs={}".format(self.version_url, ecl_param)
                params = {
                    "url": url_with_fhir_vs,
                    "count": limit
                }

                response = session.get(url, params=params)

            execution_time = time.time() - start_time

            if response.status_code == 200:
                fhir_response = response.json()

                # Convert FHIR response to Snowstorm-like format
                items = []
                expansion = fhir_response.get('expansion', {})
                contains = expansion.get('contains', [])

                for concept in contains:
                    code = concept.get('code')
                    display = concept.get('display', 'Unknown')

                    # Extract FSN and PT from designations
                    fsn = display
                    pt = display

                    for designation in concept.get('designation', []):
                        use = designation.get('use', {})
                        use_code = use.get('code', '')

                        if use_code == '900000000000003001':  # FSN
                            fsn = designation.get('value', fsn)
                        elif use_code == '900000000000013009':  # PT
                            pt = designation.get('value', pt)

                    items.append({
                        'conceptId': code,
                        'fsn': {'term': fsn},
                        'pt': {'term': pt}
                    })

                total = expansion.get('total', len(items))

                return {
                    'items': items,
                    'total': total,
                    'execution_time': execution_time
                }
            else:
                print("  Error: {} - {}".format(response.status_code, response.text))
                return {"items": [], "total": 0, "execution_time": execution_time}
        except Exception as e:
            print("  Error: {}".format(str(e)))
            return {"items": [], "total": 0, "execution_time": time.time() - start_time}

    def get_concept_details(self, concept_id):
        """
        Get concept details from OntoServer using CodeSystem $lookup.
        """
        url = "{}/CodeSystem/$lookup".format(self.base_url)

        # For $lookup, use the code system URL, and optionally version
        params = {
            "system": self.code_system_url,
            "code": concept_id,
            "version": self.version_url
        }

        try:
            session = self._get_session()
            response = session.get(url, params=params)

            if response.status_code == 200:
                fhir_response = response.json()

                display = fhir_response.get('parameter', [{}])[0].get('valueString', 'Unknown')

                # Extract FSN and PT from designations
                fsn = display
                pt = display

                for param in fhir_response.get('parameter', []):
                    if param.get('name') == 'designation':
                        for part in param.get('part', []):
                            if part.get('name') == 'use':
                                use_code = part.get('valueCoding', {}).get('code', '')
                                if use_code == '900000000000003001':  # FSN
                                    for p2 in param.get('part', []):
                                        if p2.get('name') == 'value':
                                            fsn = p2.get('valueString', fsn)
                                elif use_code == '900000000000013009':  # PT
                                    for p2 in param.get('part', []):
                                        if p2.get('name') == 'value':
                                            pt = p2.get('valueString', pt)

                return {
                    'concept_id': concept_id,
                    'fsn': fsn,
                    'pt': pt
                }
            else:
                return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}
        except Exception as e:
            print("    Warning: Could not get details for {}: {}".format(concept_id, str(e)))
            return {'concept_id': concept_id, 'fsn': 'Unknown', 'pt': 'Unknown'}


def create_adapter(server_type, **kwargs):
    """
    Factory function to create the appropriate terminology server adapter.

    Args:
        server_type: 'loincsnomed' or 'ontoserver'
        **kwargs: Server-specific configuration

    Returns:
        TerminologyServerAdapter instance

    Examples:
        # LOINCSNOMED Snowstorm (public)
        adapter = create_adapter('loincsnomed')
        adapter = create_adapter('loincsnomed', branch='MAIN/LOINC/2025-09-21')

        # MII OntoServer (production) - GET method
        adapter = create_adapter('ontoserver',
                                base_url='https://ontoserver.mii-termserv.de/fhir',
                                version_url='http://snomed.info/sct/11010000107/version/20250921')

        # MII OntoServer (staging) - GET method
        adapter = create_adapter('ontoserver',
                                base_url='https://ontoserver-staging.mii-termserv.de/fhir',
                                version_url='http://snomed.info/sct/11010000107/version/20250921')

        # MII OntoServer - POST method with ValueSet body
        adapter = create_adapter('ontoserver',
                                base_url='https://ontoserver.mii-termserv.de/fhir',
                                version_url='http://snomed.info/sct/11010000107/version/20250921',
                                use_post=True)
    """
    if server_type.lower() == 'loincsnomed':
        return LOINCSNOMEDSnowstormAdapter(**kwargs)
    elif server_type.lower() == 'ontoserver':
        return OntoServerAdapter(**kwargs)
    else:
        raise ValueError("Unknown server type: {}. Use 'loincsnomed' or 'ontoserver'".format(server_type))
