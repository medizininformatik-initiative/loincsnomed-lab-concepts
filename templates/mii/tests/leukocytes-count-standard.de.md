* **„Leukocytes other" ist drin und sollte es nicht sein.** 30406-3, 51383-8 und 729-4 zählen die *übrigen* Zellen eines Differentialblutbilds, nicht die Gesamtleukozytenzahl, doch die LOINC Ontology modelliert ihre Component als Leukocyte. Sie brauchen einen expliziten Ausschluss oder einen Change Request für eine spezifischere Component.
* **Korrigierte Zählungen sind drin.** 12227-5, 33256-9 und 66768-3 (korrigiert um kernhaltige Erythrozyten) sind dieselbe Messung nach Korrektur; sie im Routinetest zu belassen ist vertretbar, das Zusammenfassen mit unkorrigierten Werten eine Entscheidung des Datennutzers.
* **Nabelschnurblut** (47281-1, 66768-3) ist drin.
* **Fetales Blut** (61182-2) hat in diesem Release kein Direct site.
