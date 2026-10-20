Diese Seite listet die {{N_TESTS}} ValueSets des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html), die jeweils **einen klinischen Test** beschreiben, und das für jeden abgeleitete Observation-Profil. Die Regel hinter jedem ValueSet ist in ihre Attribute zerlegt dargestellt; die Konstruktion ist unter [Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt.

### Was als ein klinischer Test gilt

Ein klinischer Test ist hier das, was eine Klinikerin meint, wenn sie einen Wert anfordert oder liest: *das* Hämoglobin, *das* Kalium, *das* Gesamt-PSA. Er ist definiert durch die Component plus eine **Stufe**:

* **standard**: der Routinewert. Ein ValueSet je Analyt, eingeengt auf das übliche Material, die übliche Property und Skala (zum Beispiel Hämoglobin als Massenkonzentration im Blut, quantitativ).
* **specialized**: eine klinisch eigenständige Variante, die nicht mit dem Standardwert zusammengefasst werden darf und deshalb ein eigenes ValueSet bekommt: freies PSA, der Quotient freies/Gesamt-PSA, die LDH-Isoenzyme, das Differentialblutbild.

Jeder Test ist ein ValueSet und ein von [Laboruntersuchung](StructureDefinition-mii-pr-labor-laboruntersuchung.html) abgeleitetes Observation-Profil. Das Profil bindet `Observation.code` mit der Stärke *required* an das ValueSet, beschränkt `value[x]` auf den Datentyp, den der Test liefert, und nennt die erwartete UCUM-Einheit in einem Kommentar. Alles andere ist vom Modulprofil geerbt; die abgeleiteten Profile fügen keine neuen Elemente hinzu.

### Wie man sie verwendet

* **Implementierende, die einen lokalen Katalog mappen**, wählen das ValueSet des Tests und darin den LOINC-Code, dessen Material, Property und Methode zum lokalen Verfahren passen. Die Attributspalten unten sagen, was alle Codes der Menge gemeinsam haben; die verbleibenden Unterschiede (venöses gegenüber arteriellem Blut, Berechnung gegenüber Messung) sind die, die lokal zu entscheiden sind.
* **Validierung**: Eine Observation, die ein abgeleitetes Profil in `meta.profile` beansprucht, wird gegen die LOINC-Aufzählung des ValueSets geprüft. Das Beispiel [Laborergebnis: Hämoglobin](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html) entspricht dem Hämoglobin-Profil.
* **Datennutzer**, die den Routinewert eines Analyten wollen, nehmen das *standard*-ValueSet; für breiteres Zusammenfassen siehe die [Use-Case-ValueSets](loinc-ontology-use-cases.html).

### Die Tests

Die Attributspalten zeigen die Regel; `<<` steht für „dieses Konzept und seine Subtypen", ein bloßer Name für eine exakte Übereinstimmung. *LOINC* ist die Zahl der LOINC-Codes im ValueSet, *nur SNOMED* die Zahl der Observables der LOINC Ontology ohne LOINC-Code.

{{TESTS_TABLE}}

### Review-Hinweise

* **Stufen- und Materialwahl** sind klinische Entscheidungen. Sie sind in der Regel sichtbar und werden durch deren Änderung geändert; die Tabelle wird neu erzeugt.
* **MCH, MCHC und MCV** haben kein Material in ihrer Regel: MCH ist Hämoglobin mit der Property *entitic mass* (Masse je Zelle), die beiden anderen sind in der LOINC Ontology eigene Observable-Konzepte und werden als Fokuskonzept statt über die Component selektiert.
* **Das Differentialblutbild** ist in der LOINC Ontology ein Konzept auf Auftragsebene (eine Component ohne Property) und hat dort derzeit keinen LOINC-Code; sein ValueSet enthält zwei SNOMED-CT-Codes. Die einzelnen Differentialergebnisse (Neutrophile, Lymphozyten und so weiter) sind eigene Observables und wären jeweils ein eigener klinischer Test.
* **Nitrit im Urin** ist der einzige qualitative Test der Menge; sein Profil beschränkt den Wert auf `CodeableConcept`, zu kodieren mit den [kodierten Laborergebnissen](ValueSet-mii-vs-labor-laborergebnis-codiert.html) des Moduls.
