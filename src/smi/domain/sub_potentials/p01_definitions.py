from smi.domain.schema.sub_potential  import LLMPotenzialRatingLogic, SheetMetalSubPotential, CheckpointTyp

SP01_01_REPLACE_WELD_WITH_BEND = SheetMetalSubPotential(
    subpotential_id="SP01_01",
    subpotential_name="90°-Schweißverbindung durch Biegung ersetzen",
    checkpoint_typ=CheckpointTyp.QUALITATIV,
    llm_evaluation_goal=(
        "Bewerten, ob zwei separate Blechteile, die rechtwinklig miteinander "
        "verschweißt sind, zu einem einzigen Biegeteil zusammengeführt werden "
        "können, um die Teileanzahl zu reduzieren."
    ),
    llm_check_method=(
        "Suche im Bild/CAD nach separaten Blechteilen, die an einer rechtwinkligen, "
        "ca. 90°-Kante durch eine Schweißverbindung verbunden sind. Prüfe, ob diese "
        "Verbindung stattdessen als Biegelinie eines zusammenhängenden Blechteils "
        "darstellbar wäre. Nutze, falls vorhanden, die Abwicklung: Eine geeignete "
        "Lösung zeigt eine gemeinsame Kontur mit Biegelinie statt zwei getrennter Teile."
    ),
    llm_potenzial_rating_logic=LLMPotenzialRatingLogic(
        high=(
            "Hohes Potenzial, wenn mindestens eine klare 90°-Schweißverbindung "
            "zwischen separaten Blechteilen sichtbar ist und die beiden Flächen "
            "plausibel durch eine Biegung zu einem Teil zusammengeführt werden können."
        ),
        medium=(
            "Mittleres Potenzial, wenn eine mögliche rechtwinklige Schweißverbindung "
            "erkennbar ist, aber aus Bild/CAD unsicher bleibt, ob es wirklich separate "
            "Teile sind, ob die Verbindung geschweißt ist oder ob die Abwicklung als "
            "ein Teil möglich ist."
        ),
        low=(
            "Geringes Potenzial, wenn keine rechtwinklige Schweißverbindung zwischen "
            "separaten Blechteilen erkennbar ist oder die Konstruktion bereits als ein "
            "gebogenes Einzelteil ausgeführt ist."
        ),
    ),
)


SP02_01_CHANGE_GEOMETRY_INTEGRATE_ADDITIONAL_PART = SheetMetalSubPotential(
    subpotential_id="SP02_01",
    subpotential_name="Geometrie ändern und Zusatzteil integrieren",
    checkpoint_typ=CheckpointTyp.QUALITATIV,
    llm_evaluation_goal=(
        "Bewerten, ob ein separates Zusatzteil, zum Beispiel eine Stützstrebe, "
        "Lasche, Versteifung oder ein kleines Anschlussblech, durch eine einfache "
        "Geometrieänderung so positioniert werden kann, dass es nicht mehr als "
        "separates Teil ausgeführt werden muss, sondern als Bestandteil eines "
        "gebogenen Einzelteils integriert werden kann."
    ),
    llm_check_method=(
        "Suche im Bild/CAD nach separaten Zusatzteilen wie Streben, Laschen, "
        "Winkeln, Versteifungen oder Anschlussblechen, die an ein Hauptblech "
        "angeschweißt oder anderweitig gefügt sind. Prüfe, ob die Position, "
        "Ausrichtung oder Anschlussgeometrie dieses Zusatzteils so verändert "
        "werden könnte, dass die Fügeoperation durch eine Biegung ersetzt wird. "
        "Bewerte insbesondere, ob das Zusatzteil an eine geeignete Kante, "
        "Biegelinie oder Kontur des Hauptblechs verschoben und dadurch in die "
        "Abwicklung des Hauptteils aufgenommen werden könnte. Berücksichtige "
        "sichtbare Randbedingungen wie Bohrungen, Funktionsflächen, Bauraum, "
        "Montagezugänglichkeit und Anschlussflächen."
    ),
    llm_potenzial_rating_logic=LLMPotenzialRatingLogic(
        high=(
            "Hohes Potenzial, wenn ein separates Zusatzteil klar erkennbar ist, "
            "seine Funktion durch eine leicht geänderte Position oder Anschlussgeometrie "
            "offenbar erhalten bleiben kann und eine Integration als gebogene Lasche, "
            "Strebe oder Versteifung des Hauptblechs plausibel erscheint. Besonders "
            "hoch ist das Potenzial, wenn keine zwingenden Funktionsflächen, Bohrbilder "
            "oder festen Anschlusspunkte die aktuelle Lage des Zusatzteils bestimmen."
        ),
        medium=(
            "Mittleres Potenzial, wenn ein separates Zusatzteil erkennbar ist und "
            "eine Integration durch Geometrieänderung grundsätzlich möglich erscheint, "
            "aber aus Bild/CAD nicht eindeutig bewertbar ist, ob die exakte Lage für "
            "Steifigkeit, Montage, Bauraum, Lochpositionen, Anschlussflächen oder "
            "Kollisionen zwingend erforderlich ist."
        ),
        low=(
            "Geringes Potenzial, wenn kein separates Zusatzteil vorhanden ist, das "
            "durch eine Geometrieänderung integrierbar wäre, oder wenn das Zusatzteil "
            "offensichtlich zwei funktional festgelegte Anschlusspunkte verbindet. "
            "Ebenfalls gering ist das Potenzial, wenn die Geometrie bereits als "
            "einteiliges Biegeteil ausgeführt ist oder sichtbare Funktionsflächen, "
            "Bohrungen, Schnittstellen oder Bauraumgrenzen eine Lageänderung "
            "praktisch ausschließen."
        ),
    ),
)