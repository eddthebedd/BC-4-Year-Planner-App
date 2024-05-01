from dataclasses import dataclass
from typing import List

from .ApiUtilDataClasses import *

@dataclass
class CourseInfo(BaseInfo, BaseIdDescr):
    courseCode: str
    title: str
    transcriptTitle: str
    subjectAreaId: str
    unitsContentOwnerOrgIds: List[str]
    unitsContentOwnerPersonIds: List[str]
    instructorIds: List[str]
    instructorDescription: str
    learningObjectiveIds: List[str]
    levelValueId: str
    audiencePopulationIds: List[str]
    programRequirementIds: List[str]
    requisiteIds: List[str]
    coRequisiteIds: List[str]
    gradingOptionIds: List[str]
    creditOptionIds: List[str]
    hasFinalExam: bool
    finalExamId: str
    duration: TimeAmountInfo
    outOfClassHours: TimeAmountInfo
    contactHours: TimeAmountInfo
    specialTopicsCourse: bool
    pilotCourse: bool
    courseCodeSuffix: str
    repeatableForCreditRuleId: str


@dataclass
class CourseListingInfo(BaseInfo, BaseIdDescr):
    courseId: str
    courseCode: str
    subjectAreaId: str
    courseCodeSuffix: str
    isPrimary: bool


@dataclass
class OrgInfo(BaseInfo):
    id: str
    effectiveDate: datetime
    expirationDate: datetime
    shortName: str
    longName: str
    sortName: str
    longDescr: RichTextInfo
    shortDescr: RichTextInfo
    orgCodes: List[OrgCodeInfo]

@dataclass
class ResultValueInfo(BaseInfo, BaseKeyDescr):
    effectiveDate: datetime
    expirationDate: datetime
    resultScaleKey: str
    numericValue: int
    value: str
    

@dataclass
class RequirementInfo(BaseInfo, BaseIdDescr):
    parentRequirementId: str
    shortTitle: str
    longTitle: str
    code: str
    learningObjectiveIds: List[str]
    requisiteIds: List[str]
    adminOrgIds: List[str]
    resultOptionIds: List[str]
    url: str


@dataclass
class OfferingEnablerInfo(BaseInfo, BaseIdDescr):
    effectiveDate: datetime
    expirationDate: datetime
    ruleId: str
    deploymentOrgId: str
    campusId: str
    atpTypeKeys: List[str]
    startAtpId: str
    endAtpId: str
    scheduleId: str
    restrictToTargetAudience: bool
    isEvaluated: bool
    otherRestricionIds: List[str]
    

@dataclass
class ResultValuesGroupInfo(BaseInfo, BaseKeyDescr):
    effectiveDate: datetime
    expirationDate: datetime
    resultScaleKey: str
    rank: int
    explicitlyGroupedResultValueKeys: List[str]
    resultValueRange: ResultValueInfo


@dataclass
class RequisiteTranslationInfo(BaseInfo, BaseIdDescr):
    requisiteId: str
    translation: RichTextInfo
   

@dataclass
class Course:
    course: CourseInfo
    crossListings: List[CourseListingInfo]
    subjectArea: OrgInfo
    levelValue: ResultValueInfo
    requirements: List[RequirementInfo]
    offeringEnablers: List[OfferingEnablerInfo]
    unitContentOwners: List[OrgInfo]
    gradingOptions: List[ResultValuesGroupInfo]
    creditOptions: List[ResultValuesGroupInfo]
    prereqTerseTranslations: List[RequisiteTranslationInfo]
    coreqTerseTranslations: List[RequisiteTranslationInfo]

