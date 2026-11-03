Diese Seite zeigt, was das Release **{{RELEASE}}** der LOINC Ontology für jede Regel des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html) gegenüber dem vorherigen Release **{{PREV_RELEASE}}** geändert hat: wie viele Konzepte jede Regel vorher und nachher auswählt und welche Konzepte eingetreten oder ausgeschieden sind. Sie ist die Ausgabe des Release-Vergleichs des Generators, gerendert mit Fully Specified Names und LOINC-Codes, damit ein Reviewer sie ohne Terminologieserver lesen kann.

### Wie sie zu lesen ist

* Ein Konzept ist *neu*, wenn das neue Release es auswählt und das alte nicht. Die meisten Zugänge sind neue Konzepte der LOINC Ontology für Codes eines jüngeren LOINC-Releases; einige sind bestehende Konzepte, deren Attribute so umgebaut wurden, dass die Regel sie jetzt sieht.
* Ein Konzept ist *entfallen*, wenn das alte Release es auswählte und das neue nicht: Es wurde inaktiviert, oder ein Attribut, von dem die Regel abhängt, wurde entfernt oder geändert. Ein Abgang ist ein Review-Punkt für die Regel, nicht für die Daten des Moduls.
* Unveränderte Regeln stehen in der Tabelle, haben aber keine Konzeptlisten.

### Zusammenfassung

{{DELTA_TABLE}}

### Konzepte je Regel

{{DELTA_LISTS}}
