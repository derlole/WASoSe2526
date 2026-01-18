import pandas as pd

def csv_summer(csv_file, column_name):
    """
    Berechnet die Summe aller Zahlen in der Spalte "column_name" einer CSV-Datei.

    Args:
        csv_file (str): Dateiname der CSV-Datei.
        column_name (str): Name der Spalte, für die die Summe berechnet werden soll.

    Returns:
        int oder float: Die Summe aller Zahlen in der Spalte "column_name".
    """
    try:
        # Lese CSV-Datei ein
        df = pd.read_csv(csv_file)

        # Überprüfe, ob die Spalte existiert und enthält numerische Werte
        if column_name not in df.columns or (df[column_name].dtype != 'int64' and df[column_name].dtype != 'float64'):
            raise ValueError(f"Spalte '{column_name}' existiert nicht oder enthält keine numerischen Werte.")

        # Berechne die Summe der Spalte
        total = df[column_name].sum()

        return total

    except pd.errors.EmptyDataError:
        print("Die CSV-Datei ist leer.")
        return None

    except FileNotFoundError:
        print(f"Die Datei '{csv_file}' wurde nicht gefunden.")
        return None

    except Exception as e:
        print(f"Fehler: {e}")
        return None


# Beispielhafte Verwendung
csv_summer('datei.csv', 'wert')