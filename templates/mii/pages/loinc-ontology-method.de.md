Diese Seite erklärt, wie jedes ValueSet des [LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html) konstruiert ist, damit eine Leserin eine Regel prüfen, ein ValueSet auf einem Terminologieserver expandieren und die Artefakte für ein neues Release neu erzeugen kann.

### Die LOINC Ontology in einem Absatz

Die [LOINC Ontology](https://loincsnomed.org) wird gemeinsam vom Regenstrief Institute und SNOMED International veröffentlicht. Sie bildet LOINC-Laborterme als SNOMED-CT-Konzepte in einem Extension-Modul ab (Modul-ID `11010000107`), eingehängt unter *Observable entity*. Jedes Konzept trägt seinen LOINC-Code als alternativen Identifikator und ist mit denselben Attributen modelliert, aus denen ein LOINC-Term besteht. Weil die Konzepte in SNOMED CT liegen, kann die SNOMED Expression Constraint Language (ECL) sie über Attributwerte selektieren, einschließlich der Subtyp-Hierarchien des Werts.

| Attribut | SNOMED-CT-Attribut | LOINC-Part | Beispiel für `718-7` Hemoglobin [Mass/volume] in Blood |
|---|---|---|---|
| Component | `246093002` | Component | Hemoglobin (substance) |
| Property | `370130000` | Property | Mass concentration |
| Scale type | `370132008` | Scale | Quantitative value |
| Direct site | `704327008` | System | Blood specimen |
| Technique | `246501002` | Method | (keine) |
| Time aspect | `370134009` | Time | Single point in time |

### Aufbau einer Regel

Die Regel für den klinischen Test *Hämoglobinkonzentration im Blut* lautet:

```
<< 363787002 |Observable entity| :
    246093002 |Component|   = 38082009 |Hemoglobin (substance)|,
 << 704327008 |Direct site| = << 119297000 |Blood specimen|,
 << 370130000 |Property|    = << 118539007 |Mass concentration|,
 << 370132008 |Scale type|  = << 30766002 |Quantitative value|
```

Zu lesen als: jedes Observable, dessen Component genau Hemoglobin ist, dessen Material Blut oder ein Subtyp von Blut ist (venös, arteriell, kapillär), dessen Property Massenkonzentration oder ein Subtyp ist und dessen Skala quantitativ ist. `<<` bedeutet „dieses Konzept und alle seine Nachfahren", `<` „nur die Nachfahren"; ohne beides muss der Wert exakt passen. Die Wahl zwischen beidem ist eine sichtbar gemachte klinische Entscheidung: `<< 38082009` würde zusätzlich HbA1c und die Hämoglobin-Varianten einbeziehen, was für einen Hämoglobin-*Pool* gewollt ist, für den Routinetest Hämoglobin aber nicht.

{{EXAMPLE_ECL_ROWS}}

### Die drei Teile jedes ValueSets

Jedes ValueSet dieses Vorschlags hat dasselbe `compose`:

1. **LOINC-Aufzählung.** Die LOINC-Codes aller Konzepte, die die Regel selektiert, als `include` auf `http://loinc.org` mit der LOINC-Version des Moduls. Diesen Teil kann jeder FHIR-Validator und jeder Terminologieserver heute nutzen.
2. **Observables ohne LOINC-Code.** Die LOINC Ontology enthält auch Observables, für die noch kein LOINC-Code existiert. Sie sind als SNOMED-CT-Codes aufgeführt, damit das ValueSet vollständig ist und ein Standort sieht, wo ein LOINC-Antrag aussteht.
3. **Die Regel.** Die ECL als intensionales `include` auf `http://snomed.info/sct` mit `filter.property = constraint`, gepinnt auf das Release `{{VERSION_URI}}`. Sie dokumentiert, warum die Codes aus Teil 1 enthalten sind, und sie ist der Teil, der sich neu erzeugt.

Teil 1 und 2 sind die Aufzählung von Teil 3 zum genannten Release. Sie sind keine unabhängigen Quellen.

### Expandieren und validieren

* Auf einem Terminologieserver, der das Release der LOINC Ontology hält (etwa Snowstorm mit geladener LOINC-Extension oder der LOINC-Ontology-Browser), expandieren alle drei Teile, und die Expansion entspricht der Aufzählung.
* Auf einem Server ohne LOINC Ontology, etwa dem HL7-Server des IG-Builds, lassen sich die SNOMED-CT-Includes nicht auflösen, und der QA-Report des Builds markiert sie. Die LOINC-Aufzählung expandiert trotzdem, und die Validierung eines `Observation.code` mit LOINC-Code funktioniert wie gewohnt.
* Ein Validator, der `Observation.code` gegen ein abgeleitetes Profil prüft, braucht nur die LOINC-Aufzählung.

### Versionen und Neuerzeugung

Die Artefakte sind auf **LOINC Ontology {{RELEASE}}** gepinnt. Die LOINC Ontology erscheint in regelmäßigen Releases; das Modul pinnt für seine eigenen ValueSets LOINC 2.82. Ein Code, den LOINC zwischen beiden Ständen eingeführt oder abgekündigt hat, ist ein Review-Punkt, kein Versagen der Methode. Für ein neues Release führt der Generator jede Regel erneut aus, listet die Konzepte, die in jedem ValueSet hinzugekommen oder weggefallen sind, und schreibt diese Seiten neu. Der Differenzbericht zwischen zwei Releases ist mit dem Generator in [{{REPO_NAME}}]({{REPO_URL}}) veröffentlicht.

### Die Review-Tabellen lesen

Zu jedem ValueSet veröffentlicht der Generator außerdem eine Tabelle mit einer Zeile je Konzept: LOINC-Code, SCTID, Fully Specified Name, die Use-Case-Gruppe, in die es klassifiziert wurde, und die Attributwerte, die zur Klassifikation geführt haben. Diese Tabellen sind der Ort, einen einzelnen Code anzufechten; die Regel ist der Ort, eine ganze Menge anzufechten.
