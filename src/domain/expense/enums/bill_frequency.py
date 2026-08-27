from enum import Enum


class BillFrequency(str, Enum):
    """Frequency of recurring bill payments."""

    MONTHLY = 'monthly'          # Default: Luz, agua, gas, internet
    BIMONTHLY = 'bimonthly'      # Cada 2 meses
    QUARTERLY = 'quarterly'      # Cada 3 meses (trimestral)
    SEMI_ANNUAL = 'semi_annual'  # Cada 6 meses (semestral)
    ANNUAL = 'annual'            # Impuesto automotor, patentes
    SPORADIC = 'sporadic'        # Clases de inglés (cada X clases/semanas)
    CUSTOM = 'custom'            # Fechas específicas sin patrón fijo
