from rest_framework import serializers
from docquestapp.models import *
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ForeignObjectRel

# mga nagamit
class UserSignupSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(many=True, queryset=Roles.objects.all())

    class Meta(object):
        model = CustomUser
        fields = [
            'email', 'password', 'firstname', 'middlename', 'lastname',
            'campus', 'college', 'department', 'contactNumber', 'role'
        ]

class UserEditProfileSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(many=True, queryset=Roles.objects.all())

    class Meta(object):
        model = CustomUser
        fields = [
            'email', 'password', 'firstname', 'middlename', 'lastname',
            'campus', 'college', 'department', 'contactNumber', 'role'
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Roles
        fields =  ['roleID', 'code', 'role']

class UserLoginSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, source='role')

    class Meta(object):
        model = CustomUser
        fields = ['userID', 'firstname', 'lastname', 'roles']
    
class GoalsAndObjectivesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GoalsAndObjectives
        fields = ['goalsAndObjectives']

class MonitoringPlanAndScheduleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = MonitoringPlanAndSchedule
        fields = [
            'approach', 'dataGatheringStrategy', 'schedule',
            'implementationPhase'
        ]

class EvaluationAndMonitoringSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EvaluationAndMonitoring
        fields = [
            'projectSummary', 'indicators', 'meansOfVerification',
            'risksAssumptions', 'type'
        ]

class BudgetRequirementsItemsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = BudgetRequirementsItems
        fields = ['itemName', 'ustpAmount', 'partnerAmount', 'totalAmount']

class ProjectActivitiesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ProjectActivities
        fields = [
            'objective', 'involved', 'targetDate', 'personResponsible'
        ]

class ProjectManagementTeamSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ProjectManagementTeam
        fields = ['name']

class LoadingOfTrainersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = LoadingOfTrainers
        fields = [
            'faculty', 'trainingLoad', 'hours', 'ustpBudget', 'agencyBudget', 'totalBudgetRequirement'
        ]

class SignatoriesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Signatories
        fields = ['name', 'title']

class ProponentsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['firstname', 'lastname']

class NonUserProponentsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = NonUserProponents
        fields = ['name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Region
        fields = ['regionID', 'region']

class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(source='regionID', read_only=True)

    class Meta(object):
        model = Province
        fields = ['provinceID', 'province', 'region']

class GetProvinceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Province
        fields = ['provinceID', 'province']

class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(source='provinceID', read_only=True)

    class Meta(object):
        model = City
        fields = ['cityID', 'city', 'postalCode', 'province']

class GetCitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = City
        fields = ['cityID', 'city']

class BarangaySerializer(serializers.ModelSerializer):
    city = CitySerializer(source='cityID', read_only=True)

    class Meta(object):
        model = Barangay
        fields = ['barangayID', 'barangay', 'city']

class GetBarangaySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Barangay
        fields = ['barangayID', 'barangay']

class AddressSerializer(serializers.ModelSerializer):
    barangay = BarangaySerializer(source='barangayID', read_only=True)

    class Meta(object):
        model = Address
        fields = ['addressID', 'street', 'barangay']

class PostAddressSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Address
        fields = ['street', 'barangayID']

class PartnerAgencySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PartnerAgency
        fields = ['agencyID', 'agencyName', 'addressID']

class MOASerializer(serializers.ModelSerializer):
    class Meta(object):
        model = MOA
        fields = ['moaID', 'partyADescription', 'partyBDescription', 'termination']

class WitnessethSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Witnesseth
        fields = ['witnessethID', 'whereas', 'moaID']

class PartyObligationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PartyObligation
        fields = ['poID', 'obligation', 'party', 'moaID']

class EffectivitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Effectivity
        fields = ['effectiveID', 'effectivity', 'moaID']

class GetProjectLeaderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['userID', 'firstname', 'lastname']

class DeliverablesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Deliverables
        fields = ['deliverableName']

class UserProjectDeliverablesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserProjectDeliverables
        fields = ['userID', 'projectID', 'deliverableID']
        list_serializer_class = serializers.ListSerializer  # Use ListSerializer for bulk operations

class NotificationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'  # Shows the model name as a string (e.g., 'project' or 'moa')
    )

    class Meta:
        model = Notification
        fields = [
            'notificationID', 'userID', 'content_type',
            'source_id', 'message', 'status', 'timestamp'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Review
        fields = [
            'reviewID', 'contentOwnerID', 'content_type', 'source_id',
            'reviewedByID', 'reviewStatus', 'reviewDate', 'comment'
        ]

class GetProjectSerializer(serializers.ModelSerializer):
    userID = GetProjectLeaderSerializer()
    proponents = ProponentsSerializer(many=True)
    nonUserProponents = NonUserProponentsSerializer(many=True)
    projectLocationID = AddressSerializer()
    agency = PartnerAgencySerializer(many=True)
    goalsAndObjectives = GoalsAndObjectivesSerializer(many=True)
    projectActivities = ProjectActivitiesSerializer(many=True)
    projectManagementTeam = ProjectManagementTeamSerializer(many=True)
    budgetRequirements = BudgetRequirementsItemsSerializer(many=True)
    evaluationAndMonitorings = EvaluationAndMonitoringSerializer(source='evalAndMonitoring', many=True)
    monitoringPlanSchedules = MonitoringPlanAndScheduleSerializer(source='monitoringPlanSched', many=True)
    loadingOfTrainers = LoadingOfTrainersSerializer(many=True)
    signatories = SignatoriesSerializer(source='signatoryProject', many=True)

    class Meta(object):
        model = Project
        fields = [
            'userID', 'programCategory', 'projectTitle', 'projectType',
            'projectCategory', 'researchTitle', 'program', 'accreditationLevel', 'college', 'beneficiaries',  
            'targetImplementation', 'totalHours', 'background', 'projectComponent', 'targetScope',
            'ustpBudget', 'partnerAgencyBudget', 'totalBudget', 'proponents', 'nonUserProponents', 'projectLocationID',
            'agency', 'goalsAndObjectives', 'projectActivities', 'projectManagementTeam', 'budgetRequirements',
            'evaluationAndMonitorings', 'monitoringPlanSchedules', 'loadingOfTrainers', 'signatories', 'dateCreated',
            'status'
        ]

class PostProjectSerializer(serializers.ModelSerializer):
    userID = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    proponents = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    nonUserProponents = NonUserProponentsSerializer(many=True)
    projectLocationID = PostAddressSerializer()
    agency = serializers.PrimaryKeyRelatedField(queryset=PartnerAgency.objects.all(), many=True)
    goalsAndObjectives = GoalsAndObjectivesSerializer(many=True)
    projectActivities = ProjectActivitiesSerializer(many=True)
    projectManagementTeam = ProjectManagementTeamSerializer(many=True)
    budgetRequirements = BudgetRequirementsItemsSerializer(many=True)
    evaluationAndMonitorings = EvaluationAndMonitoringSerializer(many=True)
    monitoringPlanSchedules = MonitoringPlanAndScheduleSerializer(many=True)
    
    loadingOfTrainers = LoadingOfTrainersSerializer(many=True)
    signatories = SignatoriesSerializer(many=True)

    class Meta(object):
        model = Project
        fields = [
            'userID', 'programCategory', 'projectTitle', 'projectType',
            'projectCategory', 'researchTitle', 'program', 'accreditationLevel', 'college', 'beneficiaries',  
            'targetImplementation', 'totalHours', 'background', 'projectComponent', 'targetScope',
            'ustpBudget', 'partnerAgencyBudget', 'totalBudget', 'proponents', 'nonUserProponents', 'projectLocationID',
            'agency', 'goalsAndObjectives', 'projectActivities', 'projectManagementTeam', 'budgetRequirements',
            'evaluationAndMonitorings', 'monitoringPlanSchedules', 'loadingOfTrainers', 'signatories' 
        ]

    def create(self, validated_data):
        proponents_data = validated_data.pop('proponents')
        nonUserProponents_data = validated_data.pop('nonUserProponents')
        address_data = validated_data.pop('projectLocationID')
        projectLocationID = Address.objects.create(**address_data)
        agency_data = validated_data.pop('agency')
        goalsAndObjectives_data = validated_data.pop('goalsAndObjectives')
        projectActivities_data = validated_data.pop('projectActivities')
        projectManagementTeam_data = validated_data.pop('projectManagementTeam')
        budgetRequirements_data = validated_data.pop('budgetRequirements')
        evaluationAndMonitorings_data = validated_data.pop('evaluationAndMonitorings')
        monitoringPlanSchedules_data = validated_data.pop('monitoringPlanSchedules')
        loadingOfTrainers_data = validated_data.pop('loadingOfTrainers')
        signatories_data = validated_data.pop('signatories')
        
        project = Project.objects.create(projectLocationID=projectLocationID, **validated_data)

        project.agency.set(agency_data)
        project.proponents.set(proponents_data)

        for nonUserProponents_data in nonUserProponents_data:
            NonUserProponents.objects.create(project=project, **nonUserProponents_data)
        
        for goalsAndObjective_data in goalsAndObjectives_data:
            GoalsAndObjectives.objects.create(project=project, **goalsAndObjective_data)
        
        for projectActivity_data in projectActivities_data:
            ProjectActivities.objects.create(project=project, **projectActivity_data)

        for projectManagementTeam_data in projectManagementTeam_data:
            ProjectManagementTeam.objects.create(project=project, **projectManagementTeam_data)

        for budgetaryRequirement_data in budgetRequirements_data:
            BudgetRequirementsItems.objects.create(project=project, **budgetaryRequirement_data)

        for evaluationAndMonitoring_data in evaluationAndMonitorings_data:
            EvaluationAndMonitoring.objects.create(project=project, **evaluationAndMonitoring_data)

        for monitoringPlanSchedule_data in monitoringPlanSchedules_data:
            MonitoringPlanAndSchedule.objects.create(project=project, **monitoringPlanSchedule_data)

        for loadingOfTrainer_data in loadingOfTrainers_data:
            LoadingOfTrainers.objects.create(project=project, **loadingOfTrainer_data)

        for signatory_data in signatories_data:
            Signatories.objects.create(project=project, **signatory_data)

        return project

class UpdateProjectSerializer(serializers.ModelSerializer):
    userID = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    proponents = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    nonUserProponents = NonUserProponentsSerializer(many=True)
    projectLocationID = PostAddressSerializer()
    agency = serializers.PrimaryKeyRelatedField(queryset=PartnerAgency.objects.all(), many=True)
    goalsAndObjectives = GoalsAndObjectivesSerializer(many=True)
    projectActivities = ProjectActivitiesSerializer(many=True)
    projectManagementTeam = ProjectManagementTeamSerializer(many=True)
    budgetRequirements = BudgetRequirementsItemsSerializer(many=True)
    evaluationAndMonitorings = EvaluationAndMonitoringSerializer(source='evalAndMonitoring', many=True)
    monitoringPlanSchedules = MonitoringPlanAndScheduleSerializer(source='monitoringPlanSched', many=True)
    loadingOfTrainers = LoadingOfTrainersSerializer(many=True)
    signatories = SignatoriesSerializer(source='signatoryProject', many=True)

    class Meta:
        model = Project
        fields = [
            'userID', 'programCategory', 'projectTitle', 'projectType', 'projectCategory',
            'researchTitle', 'program', 'accreditationLevel', 'college', 'beneficiaries',
            'targetImplementation', 'totalHours', 'background', 'projectComponent', 'targetScope',
            'ustpBudget', 'partnerAgencyBudget', 'totalBudget', 'proponents', 'nonUserProponents',
            'projectLocationID', 'agency', 'goalsAndObjectives', 'projectActivities',
            'projectManagementTeam', 'budgetRequirements', 'evaluationAndMonitorings',
            'monitoringPlanSchedules', 'loadingOfTrainers', 'signatories'
        ]

    def update(self, instance, validated_data):
        # Pop out all the related data
        proponents_data = validated_data.pop('proponents', [])
        non_user_proponents_data = validated_data.pop('nonUserProponents', [])
        address_data = validated_data.pop('projectLocationID', {})
        agency_data = validated_data.pop('agency', [])
        goals_and_objectives_data = validated_data.pop('goalsAndObjectives', [])
        project_activities_data = validated_data.pop('projectActivities', [])
        project_management_team_data = validated_data.pop('projectManagementTeam', [])
        budget_requirements_data = validated_data.pop('budgetRequirements', [])
        evaluation_and_monitoring_data = validated_data.pop('evaluationAndMonitorings', [])
        monitoring_plan_schedules_data = validated_data.pop('monitoringPlanSchedules', [])
        loading_of_trainers_data = validated_data.pop('loadingOfTrainers', [])
        signatories_data = validated_data.pop('signatories', [])

        # Update the main project instance
        for attr, value in validated_data.items():
            # Check if the attribute is a reverse relationship and skip it if so
            if not isinstance(instance._meta.get_field(attr), ForeignObjectRel):
                setattr(instance, attr, value)
        instance.save()

        # Update related fields
        instance.agency.set(agency_data)
        instance.proponents.set(proponents_data)

        # Update or create address data
        if address_data:
            address = instance.projectLocationID
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        # Clear existing related data on update
        NonUserProponents.objects.filter(project=instance).delete()
        GoalsAndObjectives.objects.filter(project=instance).delete()
        ProjectActivities.objects.filter(project=instance).delete()
        ProjectManagementTeam.objects.filter(project=instance).delete()
        BudgetRequirementsItems.objects.filter(project=instance).delete()
        MonitoringPlanAndSchedule.objects.filter(project=instance).delete()
        LoadingOfTrainers.objects.filter(project=instance).delete()
        Signatories.objects.filter(project=instance).delete()

        # Handle EvaluationAndMonitoring updates
        EvaluationAndMonitoring.objects.filter(project=instance).delete()  # Clear existing records

        if evaluation_and_monitoring_data:
            try:
                for data in evaluation_and_monitoring_data:
                    # Logging each item to confirm data structure
                    print("Creating EvaluationAndMonitoring with data:", data)
                    EvaluationAndMonitoring.objects.create(project=instance, **data)
            except Exception as e:
                # Log the error to debug any issues during creation
                print("Error creating EvaluationAndMonitoring:", e)

        # Repopulate other related data
        for data in non_user_proponents_data:
            NonUserProponents.objects.create(project=instance, **data)
        for data in goals_and_objectives_data:
            GoalsAndObjectives.objects.create(project=instance, **data)
        for data in project_activities_data:
            ProjectActivities.objects.create(project=instance, **data)
        for data in project_management_team_data:
            ProjectManagementTeam.objects.create(project=instance, **data)
        for data in budget_requirements_data:
            BudgetRequirementsItems.objects.create(project=instance, **data)
        for data in monitoring_plan_schedules_data:
            MonitoringPlanAndSchedule.objects.create(project=instance, **data)
        for data in loading_of_trainers_data:
            LoadingOfTrainers.objects.create(project=instance, **data)
        for data in signatories_data:
            Signatories.objects.create(project=instance, **data)

        return instance


class GetProjectStatusSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Project
        fields = ['uniqueCode', 'projectTitle', 'dateCreated', 'status']