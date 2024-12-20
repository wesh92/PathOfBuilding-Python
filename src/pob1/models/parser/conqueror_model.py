from pydantic import BaseModel, Field, field_validator
import enum
import re

class ConquerorType(str, enum.Enum):
    ETERNAL = "eternal"
    KARUI = "karui"
    MARAKETH = "maraketh"
    TEMPLAR = "templar"
    VAAL = "vaal"

class Conqueror(BaseModel):
    id: str = Field(..., title="Internal Conqueror ID", description="Internal ID of the conqueror")  # Changed to str
    name: str = Field(..., title="Conqueror Name", description="Name of the conqueror")
    type: str = Field(..., title="Conqueror Type", description="Type of the conqueror")

    @field_validator('id')
    def validate_ids(cls, value: str) -> str:
        # ID can be 1-3 or a string "#_v#" where # are numbers.
        if not re.compile(r"^[1-3]$|^\d+_v\d+$").match(value):
            raise ValueError("ID must be either 1-3 or in format 'number_vnumber'")
        return value
    
    def get_numeric_id(self) -> int:
        "Returns the numeric ID of the conqueror if it is a simple numeric value"
        if self.id.isdigit():
            return int(self.id)
        raise ValueError("ID is not a simple numeric value")

conquerors = [
    Conqueror(id="1", name="xibaqua", type=ConquerorType.VAAL.value),
    Conqueror(id="2", name="zerphi", type=ConquerorType.VAAL.value),
    Conqueror(id="3", name="doryani", type=ConquerorType.VAAL.value),
    Conqueror(id="2_v2", name="ahuana", type=ConquerorType.VAAL.value),
    Conqueror(id="1", name="deshret", type=ConquerorType.MARAKETH.value),
    Conqueror(id="2", name="asenath", type=ConquerorType.MARAKETH.value),
    Conqueror(id="3", name="nasima", type=ConquerorType.MARAKETH.value),
    Conqueror(id="1_v2", name="balbala", type=ConquerorType.MARAKETH.value),
    Conqueror(id="1", name="cadiro", type=ConquerorType.ETERNAL.value),
    Conqueror(id="2", name="victario", type=ConquerorType.ETERNAL.value),
    Conqueror(id="3", name="chitus", type=ConquerorType.ETERNAL.value),
    Conqueror(id="3_v2", name="caspiro", type=ConquerorType.ETERNAL.value),
    Conqueror(id="1", name="kaom", type=ConquerorType.KARUI.value),
    Conqueror(id="2", name="rakiata", type=ConquerorType.KARUI.value),
    Conqueror(id="3", name="kiloava", type=ConquerorType.KARUI.value),
    Conqueror(id="3_v2", name="akoya", type=ConquerorType.KARUI.value),
    Conqueror(id="1", name="venarius", type=ConquerorType.TEMPLAR.value),
    Conqueror(id="2", name="dominus", type=ConquerorType.TEMPLAR.value),
    Conqueror(id="3", name="avarius", type=ConquerorType.TEMPLAR.value),
    Conqueror(id="1_v2", name="maxarius", type=ConquerorType.TEMPLAR.value)
]