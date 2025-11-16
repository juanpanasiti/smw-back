from src.application.dtos import CreditCardResponseDTO, UpdateCreditCardDTO


def updata_credit_card_dto(current: CreditCardResponseDTO, update: UpdateCreditCardDTO) -> CreditCardResponseDTO:
    for field, value in update:
        if value is not None:
            setattr(current, field, value)
    return current
