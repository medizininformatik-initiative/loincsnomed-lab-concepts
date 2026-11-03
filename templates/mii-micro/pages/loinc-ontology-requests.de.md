Diese Seite listet die {{N_QUERIES}} Regeln des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html), gruppiert nach der Anforderungsfamilie des Moduls 2027, mit dem ValueSet, das jede Regel erzeugt, und dem abgeleiteten Observation-Profil, wo es eines gibt. Die Konstruktion ist unter [Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt; jede Familie hat eine eigene Review-Seite mit der in Attribute zerlegten Regel und den Codes, die sie auswählt.

### Was als eine Anforderung zählt

Das Modul 2027 definiert ein Observation-Profil je *Frage an das Labor*: Wächst etwas (allgemeine Kultur), was ist es (allgemeine Bestimmung), ist ein benannter Erreger da (spezifische Bestimmung), wie viel davon (Keimzahl, Pathogenlast, Ct-Wert, Titer, quantitative Serologie), ist er empfindlich (phänotypische und voraussichtliche Empfindlichkeit), was war unter dem Mikroskop zu sehen (allgemeine und spezifische Mikroskopie), trägt er einen Resistenzmechanismus. Jede solche Frage ist hier eine Anforderungsfamilie. Innerhalb einer Familie gibt es absichtlich mehrere Regeln: die Regel, die das Profil binden würde, eine Obergrenze für das Review und Regeln, die zeigen, was eine Technique-Klausel gewinnt oder verliert.

### Wie man sie nutzt

* **Implementierende, die einen lokalen Katalog mappen**, nehmen das ValueSet der Anforderung und wählen darin den LOINC-Code, dessen Erreger, Material und Methode zum lokalen Verfahren passen. Die Attributtabelle auf der Familienseite sagt, was alle Codes der Menge gemeinsam haben.
* **Validierung**: Eine Observation, die in `meta.profile` ein abgeleitetes Profil beansprucht, wird gegen die LOINC-Aufzählung des gebundenen ValueSets geprüft.
* **Die Modulredaktion** vergleicht das ValueSet einer Regel mit dem modul­eigenen LOINC-ValueSet derselben Anforderung; die Abdeckungstabellen unten tun das für die aufgezählten Codes.

### Die Regeln

*LOINC* ist die Zahl der LOINC-Codes im ValueSet; *nur SNOMED* die Zahl der Observables der LOINC Ontology ohne LOINC-Code; die Delta-Spalte zählt Konzepte, die zwischen {{PREV_RELEASE}} und {{RELEASE}} in das ValueSet eingetreten oder aus ihm ausgeschieden sind.

{{REQUEST_TABLE}}

### Die abgeleiteten Profile

Jedes Profil unten ist von einem Modulprofil abgeleitet und verengt nur `Observation.code` auf das berechnete ValueSet (Bindungsstärke *required*). Wo eine Anforderung mehrere Regeln braucht, bindet das Profil ein Vereinigungs-ValueSet.

{{PROFILE_TABLE}}

### Abdeckung der aufgezählten Codes des Moduls

Das Modul zählt in mehreren seiner ValueSets LOINC-Codes auf (neben den Property-Filtern). Von diesen {{N_ENUM}} Codes sind {{N_ENUM_IN_ONTOLOGY}} in der LOINC Ontology {{RELEASE}}; der Rest ist von keiner Regel erreichbar, was immer die Regel sagt. Es fehlen unter anderem der bevorzugte methodenneutrale Code 41852-5 (*Microorganism or agent identified in Specimen*), alle Keimzahlcodes, alle Aviditätscodes und alle Resistenzdeterminanten-Codes. Die zweite Tabelle listet jeden aufgezählten Code mit seiner SCTID und den Vorschlags-ValueSets, die ihn enthalten.

{{COVERAGE_SUMMARY}}

{{COVERAGE_DETAIL}}
