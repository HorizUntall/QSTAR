from enum import Enum

class SexEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"

class UserTypeEnum(str, Enum):
    STUDENT = "student"
    FACULTY = "faculty"