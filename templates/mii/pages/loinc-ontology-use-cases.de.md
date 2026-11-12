Diese Seite listet die {{N_USECASE}} ValueSets des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html), die **Datennutzern** dienen: für jeden von {{N_ANALYTES}} Analyten abgestufte Mengen all dessen, was die LOINC Ontology auf diesen Analyten abbildet. Die Konstruktion ist unter [Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt; die engen Mengen je Laborparameter stehen unter [ValueSets je Laborparameter](loinc-ontology-clinical-tests.html).

### Der Use Case definiert die Aggregation

Ein Datenintegrationszentrum wird nach „allen Hämoglobinwerten" gefragt. Was das bedeutet, hängt von der Frage ab: Ein Kohorten-Screening will jede Observation, die überhaupt von Hämoglobin handelt; eine Längsschnittanalyse will numerische Werte; ein standortübergreifender Vergleich will nur Werte, die sich auf eine Einheit umrechnen lassen. Keine einzelne Liste bedient alle drei, und eine Liste, die eine bedient, ist für die anderen falsch.

Der Vorschlag geht deshalb vom **Kandidatenpool** eines Analyten aus, allem in der LOINC Ontology, dessen Component der Analyt ist (jede Property, jede Skala, jedes Material), und klassifiziert diesen Pool über zwei Attribute, **Scale type** und **Property**, in Gruppen, die dem entsprechen, was ein Datennutzer mit den Werten tun darf. Ein ValueSet je Analyt und Gruppe.

### Die Gruppen

| Gruppe | Regel | Was der Datennutzer bekommt |
|---|---|---|
| **Vollständig** | der ganze Pool | Obergrenze: jedes Observable zum Analyten, einschließlich panelartiger Grouper und der „Measurement of X"-Konzepte ohne Skala. Für Recall, Kohorten-Screening und als Basis, aus der die anderen Gruppen geschnitten werden. |
| **Quantitativ (alle numerischen)** | Scale type Quantitative, oder jede Mess-Property, wenn keine Skala asserted ist | Alle numerischen Ergebnisse, einschließlich Verhältnisse, Anteile und Raten. Werte lassen sich je Code auftragen, aber nicht ohne Blick auf die Einheit über Codes hinweg zusammenfassen. |
| **Quantitativ und konvertierbar** | Quantitativ mit einer Konzentrations-Property (Massen-, Stoffmengen-, Anzahl-, arbiträre oder Mengen-Konzentration), Verhältnisse und Anteile ausgeschlossen | Die Menge, deren Werte sich nach UCUM-Umrechnung zusammenfassen lassen. Die Gruppe für standortübergreifende Vergleiche und für Referenzbereichsarbeit. |
| **Qualitativ** | Scale type Ordinal oder Nominal, oder eine Nachweis- oder Threshold-Property | Nachweis oder kein Nachweis, positiv oder negativ, abgestufte Befunde. Werte sind kodiert, nicht numerisch. |
| **Semiquantitativ** | Scale type Semi-quantitative | Teststreifen-Ablesungen (0 bis ++++). Weder streng numerisch noch rein qualitativ; üblicherweise von beidem getrennt gehalten. |

Die Klassifikation wird in dieser Reihenfolge angewendet, der erste Treffer gewinnt: qualitativ, dann semiquantitativ, dann quantitativ (mit konvertierbar als Verfeinerung). Scale type ist in der LOINC Ontology nicht immer asserted; die Property als zweites Kriterium macht die Klassifikation vollständig. Über alle Analyten blieb kein Konzept unklassifiziert.

Observables mit Component, aber **ohne Property** sind Auftrags- oder Panelcodes (zum Beispiel „Differential count of white blood cells"). Sie zerfallen in mehrere Ergebnisse und sind kein einzelner Messwert; sie erscheinen in den Review-Tabellen, erhalten aber kein ValueSet.

### Die Analyte

Die Pool-Spalte zeigt die Component; `<<` steht für „dieses Konzept und seine Subtypen". Die Zellen verlinken das ValueSet und zeigen die Zahl der Konzepte.

{{USECASE_TABLE}}

### Recall gegen LOINC selbst

Eine Regel kann nur selektieren, was die LOINC Ontology modelliert, deshalb werden die Pools auch in der Gegenrichtung geprüft: Für jeden Analyten wird die LOINC-Tabelle des Release {{LOINC_VERSION}} nach den Labortermen durchsucht, die eine Laborärztin zu diesem Analyten zählen würde (über Component, wo nötig Property und System), und die Tabelle sagt, wie viele davon der Pool erreicht. Ein Term außerhalb des Pools ist mit einer anderen Component modelliert oder gar nicht; die Analyt-Seiten listen sie einzeln. Die letzte Spalte zählt, wie viele der LOINC-Terme die ValueSets je Laborparameter aufzählen; der Abstand zum Pool ist die Menge der Codes, die eine Klinikerin nicht den Routinewert nennen würde.

{{RECALL_TABLE}}

### Review-Hinweise

* **Hämatokrit** hat jetzt einen eigenen Pool: Erythrocyte mit der Property Volume fraction. Der Erythrozyten-Pool enthält die Hämatokrit-Konzepte weiterhin, und das ist korrekt, ein Hämatokrit ist ein Erythrozyten-Observable; nur sind die Hämatokrit-Use-Case-ValueSets keine Kopie der Erythrozyten-Mengen mehr.
* **MCH** wird auf der exakten Component Hemoglobin mit den beiden entitischen Properties (Masse und Stoffmenge je Zelle) gepoolt, nicht mehr auf `<< Hemoglobin`, was HbA1c und die Hämoglobin-Varianten hereingebracht hatte. Der Hämoglobin-Pool nutzt die exakte Component und enthält deshalb auch die MCH-Konzepte.
* **GFR** hat in der LOINC Ontology keine Component; ihr Pool ist jedes Observable, dessen *Process output* die GFR-Berechnung ist. **Protein im Urin** wird mit dem Material in der Pool-Definition gepoolt, weil Gesamtprotein im Serum ein anderer klinischer Parameter ist.
* **Leukozyten** hat zwei Konzepte auf Auftragsebene (das Differentialblutbild), die in den Review-Tabellen stehen und aus jeder Gruppe ausgeschlossen sind.
* **Material ist auf dieser Ebene kein Kriterium**: Hämoglobin im Urin und im Blut liegen in derselben quantitativen Gruppe. Wer ein Material braucht, engt über das ValueSet je Laborparameter oder über `Observation.specimen` ein.
