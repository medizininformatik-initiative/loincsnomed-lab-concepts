Dieser Abschnitt ist ein **Vorschlag**, kein normativer Inhalt des Moduls. Er begleitet Ballot-Kommentare zu 2027.0.0-ballot und zeigt an lauffähigen Artefakten, wie LOINC-ValueSets für `Observation.code` aus der LOINC Ontology *berechnet* werden können, statt als handgepflegte Listen vorzuliegen. Alles in diesem Abschnitt ist aus einem veröffentlichten Regelwerk generiert; nach der Generierung wurde nichts von Hand verändert.

### Das Problem, das er adressiert

Das Modul bindet `Observation.code` an LOINC, lässt aber offen, *welche* LOINC-Codes ein Standort für einen bestimmten Test verwenden soll und welche Codes ein Datennutzer zusammenfassen darf, wenn er eine Frage wie „alle Hämoglobinwerte dieses Patienten" beantwortet. Heute sind beide Antworten Listen: das MII-300-Subset, lokale Mapping-Tabellen, projektspezifische Codelisten. Listen veralten mit jedem LOINC-Release, sie sagen nicht, *warum* ein Code drin oder draußen ist, und zwei Listen für denselben Test stimmen selten überein.

Die LOINC Ontology macht die Regel selbst zum Artefakt. Jeder LOINC-Laborterm ist dort ein SNOMED-CT-Observable mit expliziten Attributen (was gemessen wird, in welchem Material, welche Property, auf welcher Skala). Ein ValueSet ist dann ein Ausdruck über diese Attribute, und seine LOINC-Aufzählung ist ein abgeleitetes Produkt, das sich für jedes Release neu erzeugen lässt.

### Was dieser Abschnitt bietet

| Seite | Inhalt | Für wen |
|---|---|---|
| [Wie die ValueSets gebaut werden](loinc-ontology-method.html) | Das Attributmodell der LOINC Ontology, der Aufbau einer ECL-Regel, die drei Teile jedes ValueSets, Expansion und Versionierung | Implementierende, Terminologen |
| [ValueSets je klinischem Test](loinc-ontology-clinical-tests.html) | {{N_TESTS}} ValueSets, eines je klinisch unterscheidbarem Test, jedes mit abgeleitetem Observation-Profil und der Regel in Attributspalten zerlegt | Implementierende, die einen lokalen Katalog mappen; Validierung |
| [Use-Case-ValueSets je Analyt](loinc-ontology-use-cases.html) | {{N_USECASE}} ValueSets über {{N_ANALYTES}} Analyte, abgestuft danach, was ein Datennutzer zusammenfassen darf: alles, numerisch, einheitenkonvertierbar, qualitativ, semiquantitativ | Forschende, Datenintegrationszentren |

Eine ausgearbeitete Beispielinstanz, [Laborergebnis: Hämoglobin (LOINC-Ontology-Profil)](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html), zeigt ein Ergebnis, das einem der abgeleiteten Profile entspricht.

### Auf einen Blick

* Verwendetes Release: **LOINC Ontology {{RELEASE}}** (`{{VERSION_URI}}`); der LOINC-Pin des Moduls ist 2.82.
* Jedes ValueSet trägt die LOINC-Aufzählung, die Observables der LOINC Ontology ohne LOINC-Code und die Regel selbst als intensionales SNOMED-CT-Include.
* Alle Artefakte sind `draft` und `experimental`. Ihre kanonischen URLs folgen dem Modulmuster und wären stabil, falls das Modul sie übernimmt.
* Generator, Regelwerk und Review-Tabellen je Konzept: [{{REPO_NAME}}]({{REPO_URL}}).

### Was ein Reviewer beurteilen soll

1. Ist eine berechnete, regelbasierte Definition der richtige Weg für das Modul, festzulegen, welche LOINC-Codes zu einem Test gehören?
2. Sind die zwei Ebenen, klinischer Test und Use Case, die richtige Granularität für Implementierende und für Datennutzer?
3. Welche der Pool-Definitionen und Stufenentscheidungen auf den folgenden Seiten sollte das Modul anders treffen? Jede Entscheidung ist als Regel sichtbar und wird durch Ändern dieser Regel geändert.
