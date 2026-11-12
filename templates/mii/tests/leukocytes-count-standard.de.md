* **„Leukocytes other" ist drin und sollte es nicht sein.** 30406-3, 51383-8 und 729-4 zählen die *übrigen* Zellen eines Differentialblutbilds, nicht die Gesamtleukozyten, doch die LOINC Ontology modelliert ihre Component als Leukocyte. Kein Attribut trennt sie; sie brauchen eine explizite Ausschlussliste oder einen Change Request für eine spezifischere Component.
* **Korrigierte Zählungen sind drin.** 12227-5 und 33256-9 (korrigiert um kernhaltige Erythrozyten) sind dieselbe Messung nach Korrektur; sie im Routinetest zu behalten ist vertretbar, sie mit unkorrigierten Werten zusammenzufassen eine Entscheidung des Datennutzers.
* **Nabelschnurblut** (47281-1, 66768-3) ist über den Blut-Block draußen.
* **Fetales Blut** (61182-2) hat in diesem Release kein Direct site.
