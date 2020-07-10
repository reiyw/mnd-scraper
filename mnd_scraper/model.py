from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config, LetterCase
from marshmallow import fields


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class SpeechRecord:
    speaker: str
    speaker_yomi: Optional[str]
    speaker_group: Optional[str]
    speaker_role: Optional[str]
    speech: str
    speech_url: str = field(metadata=config(field_name="speechURL"))
    speech_id: str = field(metadata=config(field_name="speechID"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class MeetingRecord:
    image_kind: str
    name_of_house: str
    name_of_meeting: str
    issue: str
    speech_record: List[SpeechRecord]
    issue_id: str = field(metadata=config(field_name="issueID"))
    date: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Response:
    number_of_records: int
    meeting_record: Optional[List[MeetingRecord]] = None
