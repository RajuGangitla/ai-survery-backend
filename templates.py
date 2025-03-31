from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SurveyEndScreenCard(BaseModel):
    """
    Represents the ending screen of a survey.
    This is displayed to users after they complete the survey.
    """
    id: str = Field(
        default_factory=lambda: "default_id",  # Placeholder for `createId()`
        description="A unique identifier for the ending card. This should be generated dynamically in practice."
    )
    type: str = Field(
        default="endScreen",
        description="The type of the card. For ending cards, this is always 'endScreen'."
    )
    headline: str = Field(
        ...,
        description="The main text displayed on the ending card. This is typically a thank-you message."
    )
    subheader: Optional[str] = Field(
        None,
        description="Additional explanatory text displayed below the headline. This is optional."
    )
    buttonLabel: str = Field(
        ...,
        description="The label for the button displayed on the ending card (e.g., 'Close' or 'Finish')."
    )
    buttonLink: str = Field(
        default= "https://formbricks.com",
        description="The URL the button links to when clicked. This could redirect users to a website or close the survey."
    )

class SurveyWelcomeCard(BaseModel):
    """
    Represents the welcome card displayed at the beginning of a survey.
    This card can include a headline, HTML content, and a button to start the survey.
    """
    enabled: bool = Field(
        default=False,
        description="Indicates whether the welcome card is enabled. If False, the card will not be displayed."
    )
    headline: Optional[str] = Field(
        None,
        description="The main text displayed on the welcome card. Typically used as an introductory message."
    )
    html: Optional[str] = Field(
        None,
        description="HTML content displayed on the welcome card. This can include rich text or embedded media."
    )
    buttonLabel: Optional[str] = Field(
        None,
        description="The label for the button displayed on the welcome card (e.g., 'Start Survey')."
    )
    timeToFinish: bool = Field(
        default=False,
        description="Indicates whether the estimated time to complete the survey should be displayed."
    )
    showResponseCount: bool = Field(
        default=False,
        description="Indicates whether the number of responses collected so far should be displayed."
    )


class HiddenFields(BaseModel):
    """
    Represents hidden fields in a survey.
    These fields are used for tracking or metadata purposes.
    """
    enabled: bool = Field(
        default=True,
        description="Indicates whether hidden fields are enabled."
    )
    fieldIds: List[str] = Field(
        default_factory=list,
        description="List of field IDs for hidden fields."
    )

class SurveyPreset(BaseModel):
    """
    Represents the default preset for a new survey.
    This includes the welcome card, ending cards, hidden fields, and questions.
    """
    name: str = Field(
        default="New Survey",
        description="The name of the survey preset. Defaults to 'New Survey'."
    )
    welcomeCard: SurveyWelcomeCard = Field(
        ...,
        description="The welcome card displayed at the beginning of the survey."
    )
    endings: List[SurveyEndScreenCard] = Field(
        ...,
        description="A list of ending cards displayed after the survey is completed."
    )
    hiddenFields: HiddenFields = Field(
        ...,
        description="Hidden fields used for tracking or metadata purposes."
    )
    questions: List[Dict] = Field(
        default_factory=list,
        description="A list of questions included in the survey. Starts as an empty list."
    )

# Base class for reusable IDs
class ReusableId(BaseModel):
    id: str = Field(default_factory=lambda: "default_id", description="A unique identifier.")

# Base class for survey conditions
class SurveyCondition(BaseModel):
    id: str = Field(default_factory=lambda: "default_id", description="A unique identifier for the condition.")
    leftOperand: Dict[str, str] = Field(..., description="The left operand in the condition (e.g., question ID).")
    operator: str = Field(..., description="The operator used in the condition (e.g., 'isSkipped', 'equals').")
    rightOperand: Optional[Dict[str, str]] = Field(None, description="The right operand in the condition (optional).")

# Base class for survey logic
class SurveyLogic(BaseModel):
    id: str = Field(default_factory=lambda: "default_id", description="A unique identifier for the logic.")
    conditions: Dict[str, List[SurveyCondition]] = Field(..., description="Conditions that determine the logic flow.")
    actions: List[Dict[str, str]] = Field(..., description="Actions to take when conditions are met.")

# Base class for survey choices
class SurveyChoice(BaseModel):
    id: str = Field(default_factory=lambda: "default_id", description="A unique identifier for the choice.")
    label: str = Field(..., description="The text displayed for the choice.")

# Base class for survey questions
class SurveyQuestion(BaseModel):
    id: str = Field(default_factory=lambda: "default_id", description="A unique identifier for the question.")
    type: str = Field(..., description="The type of the question (e.g., 'CTA', 'MultipleChoiceSingle').")
    headline: str = Field(..., description="The main text of the question.")
    subheader: Optional[str] = Field(None, description="Additional explanatory text below the headline.")
    required: bool = Field(..., description="Whether the question must be answered.")
    buttonLabel: Optional[str] = Field(None, description="The label for the button associated with the question.")
    backButtonLabel: Optional[str] = Field(None, description="The label for the back button.")
    dismissButtonLabel: Optional[str] = Field(None, description="The label for the dismiss button.")
    html: Optional[str] = Field(None, description="HTML content for CTA-type questions.")
    charLimit: Optional[Dict[str, bool]] = Field(None, description="Character limit configuration for OpenText questions.")
    inputType: Optional[str] = Field(None, description="Input type for OpenText questions (e.g., 'text', 'email').")
    longAnswer: Optional[bool] = Field(None, description="Indicates whether the answer can be long.")
    placeholder: Optional[str] = Field(None, description="Placeholder text for OpenText questions.")
    scale: Optional[str] = Field(None, description="Scale type for Rating questions (e.g., 'number', 'star').")
    range: Optional[int] = Field(None, description="Range for Rating questions (e.g., 5).")
    lowerLabel: Optional[str] = Field(None, description="Lower label for Rating questions.")
    upperLabel: Optional[str] = Field(None, description="Upper label for Rating questions.")
    shuffleOption: Optional[str] = Field(None, description="Shuffle option for MultipleChoice questions.")
    choices: Optional[List[SurveyChoice]] = Field(None, description="List of answer choices for MultipleChoice questions.")
    logic: Optional[List[SurveyLogic]] = Field(None, description="Conditional logic for the question.")
    label: Optional[str] = Field(None, description="Label for Consent-type questions.")

# Base class for survey presets
class SurveyPreset(BaseModel):
    name: str = Field(..., description="The name of the survey preset.")
    welcomeCard: Optional[Dict] = Field(None, description="The welcome card displayed at the start of the survey.")
    endings: List[Dict] = Field(..., description="List of ending cards displayed after the survey.")
    hiddenFields: Optional[Dict] = Field(None, description="Hidden fields used for tracking or metadata.")
    questions: List[SurveyQuestion] = Field(..., description="List of questions in the survey.")

# Base class for the Cart Abandonment Survey
class CartAbandonmentSurvey(BaseModel):
    name: str = Field(..., description="The name of the survey.")
    role: str = Field(..., description="The role of the person responsible for creating the survey.")
    industries: List[str] = Field(..., description="The industries the survey is relevant to.")
    channels: List[str] = Field(..., description="Where the survey will be distributed.")
    description: str = Field(..., description="A brief description of the survey's purpose.")
    preset: SurveyPreset = Field(..., description="The preset configuration for the survey.")