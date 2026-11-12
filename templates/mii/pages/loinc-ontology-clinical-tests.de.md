Diese Seite listet die {{N_TESTS}} ValueSets des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html), die jeweils **einen Laborparameter** (englisch: *clinical test*) beschreiben, und das für jeden abgeleitete Observation-Profil. Die Regel hinter jedem ValueSet ist in ihre Attribute zerlegt dargestellt; die Konstruktion und die gemeinsamen Bausteine sind unter [Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt.

### Was als ein Laborparameter gilt

Ein Laborparameter ist hier das, was eine Klinikerin meint, wenn sie einen Wert anfordert oder liest: *das* Hämoglobin, *das* Kalium, *das* Gesamt-PSA. Ein Parameter ist eine Zeile im Laborbefund, und seine Codes sind die, deren Werte als dieselbe Größe gelesen werden können. Er ist definiert durch die Component plus eine **Stufe**:

* **standard**: der Routinewert. Ein ValueSet je Analyt, eingeengt auf das übliche Material, die übliche Property und Skala. Seit dem klinischen Review teilen die Standardtests zwei Bausteine: Das Material ist *Blut und seine Subtypen, Serum und Plasma eingeschlossen, Nabelschnurblut, fetales Blut und Trockenblut ausgeschlossen*, und die Property ist *jede Konzentration* (Masse, Stoffmenge oder arbiträr), damit g/dL- und mmol/L-Codes derselben Messung in einer Menge liegen und die Einheit der UCUM-Umrechnung überlassen bleibt.
* **specialized**: eine klinisch eigenständige Variante, die nicht mit dem Standardwert zusammengefasst werden darf und deshalb ein eigenes ValueSet bekommt: freies PSA, der Quotient freies/Gesamt-PSA, die LDH-Isoenzyme, das Differentialblutbild, der Protein/Kreatinin-Quotient, Hämoglobin im Nabelschnurblut.

Jeder Parameter ist ein ValueSet und ein von [Laboruntersuchung](StructureDefinition-mii-pr-labor-laboruntersuchung.html) abgeleitetes Observation-Profil. Das Profil bindet `Observation.code` mit der Stärke *required* an das ValueSet, beschränkt `value[x]` auf den Datentyp, den der Test liefert, und nennt die erwartete UCUM-Einheit in einem Kommentar. Alles andere ist vom Modulprofil geerbt; die abgeleiteten Profile fügen keine neuen Elemente hinzu.

### Wie man sie verwendet

* **Implementierende, die einen lokalen Katalog mappen**, wählen das ValueSet des Parameters und darin den LOINC-Code, dessen Material, Property und Methode zum lokalen Verfahren passen. Die Attributspalten unten sagen, was alle Codes der Menge gemeinsam haben; die verbleibenden Unterschiede (venöses gegenüber arteriellem Blut, Berechnung gegenüber Messung, g/dL gegenüber mmol/L) sind die, die lokal zu entscheiden sind.
* **Validierung**: Eine Observation, die ein abgeleitetes Profil in `meta.profile` beansprucht, wird gegen die LOINC-Aufzählung des ValueSets geprüft. Das Beispiel [Laborergebnis: Hämoglobin](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html) entspricht dem Hämoglobin-Profil.
* **Datennutzer**, die den Routinewert eines Analyten wollen, nehmen das *standard*-ValueSet; für breiteres Zusammenfassen siehe die [Use-Case-ValueSets](loinc-ontology-use-cases.html).

### Die Laborparameter

Die Attributspalten zeigen die Regel; `<<` steht für „dieses Konzept und seine Subtypen", ein bloßer Name für eine exakte Übereinstimmung, `minus` für einen Ausschluss innerhalb des Werts. *LOINC* ist die Zahl der LOINC-Codes im ValueSet (von Hand ergänzte Ontologie-Lücken eingeschlossen), *nur SNOMED* die Zahl der Observables der LOINC Ontology ohne LOINC-Code. Der Testname verlinkt die Review-Seite des Analyten mit jedem enthaltenen und ausgeschlossenen Code samt Begründung.

{{TESTS_TABLE}}

### Review-Hinweise

* **Stufen- und Materialwahl** sind klinische Entscheidungen. Sie sind in der Regel sichtbar und werden durch deren Änderung geändert; die Tabelle wird neu erzeugt.
* **Offen für das klinische Review**: ob die Thrombozytenzahl Plasma und thrombozytenreiches Plasma ausschließen soll (drei transfusionsmedizinische Codes), und ob die LDH-Isoenzyme auf Serum und Plasma beschränkt werden sollen (21 Codes in Urin, Liquor und Ergüssen fallen weg). Beides steht als Regel da und wird auf den Analyt-Seiten diskutiert.
* **Was die Ontologie nicht ausdrücken kann.** Der LOINC-Part für *Belastung* und *Zeitpunkt* ist kein Attribut der LOINC Ontology: Der Kreatinin-Test enthält deshalb 71 Zeitpunkt- und Belastungscodes neben den acht Routinecodes. Auch LOINCs *Status* (active, discouraged) ist kein Attribut: Ein discouraged Kalium-Code und zwei discouraged GFR-Codes passieren ihre Regeln. Beides wäre über einen Filter auf der LOINC-Tabelle im Generator zu behandeln, eine Entscheidung des Moduls, nicht einer Regel.
* **Ontologie-Lücken.** Einen LOINC-Code, den das Release nicht modelliert, erreicht keine Regel. Die molare MCHC (59467-1) ist so ein Code; er ist seinem ValueSet von Hand hinzugefügt, am ValueSet und auf der Analyt-Seite als Ontologie-Lücke markiert und an die Pflege der LOINC Ontology gemeldet.
* **MCHC und MCV** haben keine Component in ihrer Regel: Beide sind in der LOINC Ontology eigene Observable-Konzepte (MCHC über *Inheres in* = Hemoglobin) und werden als Fokuskonzept selektiert. **MCH** ist Hämoglobin mit den entitischen Properties auf dem Erythrozyten-Specimen. **Die eGFR** hat gar keine Component; sie wird über *Process output* = Glomerular filtration rate (calculation) selektiert.
* **Das Differentialblutbild** ist in der LOINC Ontology ein Konzept auf Auftragsebene (eine Component ohne Property) und hat dort derzeit keinen LOINC-Code; sein ValueSet enthält zwei SNOMED-CT-Codes. Die einzelnen Differentialergebnisse (Neutrophile, Lymphozyten und so weiter) sind eigene Observables und wären jeweils ein eigener Laborparameter.
* **Nitrit im Urin** ist der einzige qualitative Parameter der Menge; sein Profil beschränkt den Wert auf `CodeableConcept`, zu kodieren mit den [kodierten Laborergebnissen](ValueSet-mii-vs-labor-laborergebnis-codiert.html) des Moduls.
