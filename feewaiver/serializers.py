from ledger.accounts.models import EmailUser
from rest_framework import serializers

from feewaiver.models import (
        ContactDetails, 
        FeeWaiver,
        FeeWaiverVisit,
        FeeWaiverUserAction,
        FeeWaiverLogEntry,
        Participants,
        Park,
        CampGround,
        )
from feewaiver.main_models import TemporaryDocumentCollection
#from disturbance.components.organisations.models import (
 #                               Organisation
  #                          )
from feewaiver.main_serializers import CommunicationLogEntrySerializer
from rest_framework import serializers


class EmailUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EmailUser
        fields = (
                'id',
                'email',
                'first_name',
                'last_name',
                'title',
                'organisation',
                'name'
                )

    def get_name(self, obj):
        return obj.get_full_name()


class FeeWaiverUserActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = FeeWaiverUserAction
        fields = '__all__'


class FeeWaiverLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()
    class Meta:
        model = FeeWaiverLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]

class ContactDetailsSaveSerializer(serializers.ModelSerializer):
    participants_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ContactDetails
        fields = (
                'id',
                'organisation',
                'organisation_description',
                'contact_name',
                'postal_address',
                'suburb',                     
                'state',                     
                'postcode',                     
                'phone',
                'email',
                'email_confirmation',
                'participants_id',
                'organisation_description'
                )
        read_only_fields = (
            'id',
        )

    def get_participants_code(self,obj):
        return obj.participants_id

class ContactDetailsSerializer(serializers.ModelSerializer):
    participants_id = serializers.IntegerField(write_only=True)
    participants_code = serializers.SerializerMethodField()
    #        required=True, write_only=True, allow_null=False)

    class Meta:
        model = ContactDetails
        fields = (
                'id',
                'organisation',
                'organisation_description',
                'contact_name',
                'postal_address',
                'suburb',                     
                'state',                     
                'postcode',                     
                'phone',
                'email',
                'email_confirmation',
                'participants_id',
                'participants_code',
                'organisation_description'
                )
        read_only_fields = (
            'id',
        )

    def get_participants_code(self,obj):
        return obj.participants_id


class ParkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Park
        fields = (
                'id',
                'name',
                'entrance_fee',
                )
        read_only_fields = (
            'id',
        )


class CampGroundSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampGround
        fields = (
                'id',
                'name',
                'park_id',
                )
        read_only_fields = (
            'id',
        )


class FeeWaiverVisitSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeeWaiverVisit
        fields = (
                'id',
                #'fee_waiver_id',
                'description',     
                'camping_requested',
                'date_from',     
                'date_to',     
                'issued',
                'index',
                #'selected_park_ids',    
                'number_of_vehicles',     
                'number_of_participants',     
                'age_of_participants_array', 
                #'camping_assessment_choices',
                'camping_assessment',
                )
        read_only_fields = (
            'id',
        )


class FeeWaiverVisitSerializer(serializers.ModelSerializer):
    selected_park_ids = serializers.SerializerMethodField()
    selected_free_park_ids = serializers.SerializerMethodField()
    #selected_campground_ids = serializers.SerializerMethodField()
    selected_park_names = serializers.SerializerMethodField()
    selected_free_park_names = serializers.SerializerMethodField()
    #selected_campground_names = serializers.SerializerMethodField()
    fee_waiver_id = serializers.IntegerField(
            required=True, write_only=True, allow_null=False)
    camping_approved = serializers.SerializerMethodField()
    #camping_assessment_choices = serializers.SerializerMethodField()


    class Meta:
        model = FeeWaiverVisit
        fields = (
                'id',
                'fee_waiver_id',
                'description',     
                'camping_requested',
                'date_from',     
                'date_to',     
                'selected_park_ids',    
                'selected_free_park_ids',    
                #'selected_campground_ids',    
                'selected_park_names',    
                'selected_free_park_names',    
                #'selected_campground_names',    
                'number_of_vehicles',     
                'number_of_participants',     
                'age_of_participants_array', 
                #'camping_assessment_choices',
                'camping_assessment',
                'camping_approved',
                'issued',
                'index',
                )
        read_only_fields = (
            'id',
        )

    def get_selected_park_ids(self, obj):
        park_id_list = []
        for park in obj.parks.all():
            park_id_list.append(str(park.id))
        return park_id_list

    def get_selected_free_park_ids(self, obj):
        park_id_list = []
        for park in obj.free_parks.all():
            park_id_list.append(str(park.id))
        return park_id_list

    #def get_selected_campground_ids(self, obj):
    #    campground_id_list = []
    #    for campground in obj.campgrounds.all():
    #        campground_id_list.append(str(campground.id))
    #    return campground_id_list

    def get_selected_park_names(self, obj):
        park_name_list = []
        for park in obj.parks.all():
            park_name_list.append(str(park.name))
        return park_name_list

    def get_selected_free_park_names(self, obj):
        park_name_list = []
        for park in obj.free_parks.all():
            park_name_list.append(str(park.name))
        return park_name_list

    #def get_selected_campground_names(self, obj):
    #    campground_name_list = []
    #    for campground in obj.campgrounds.all():
    #        campground_name_list.append(str(campground.name))
    #    return campground_name_list

    def get_camping_approved(self, obj):
        choices=FeeWaiverVisit.CAMPING_CHOICES
        approved_text = ""
        for i in choices:
            if i[0]==obj.camping_assessment:
                approved_text = i[1]
        return approved_text


class FeeWaiverSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'lodgement_date',
                #'contact_details_id',     
                'fee_waiver_purpose',     
                'comments_to_applicant',
                #'visits',
                #'processing_status',
                #'can_process',
                #'assigned_officer',
                #'assigned_officer_id',
                #'action_group',
                #'current_officer',
                )
        read_only_fields = (
            'id',
            'lodgement_number',
            'lodgement_date',
        )


class FeeWaiverMinimalSerializer(serializers.ModelSerializer):
    processing_status = serializers.SerializerMethodField()
    proposed_status = serializers.SerializerMethodField()
    can_process = serializers.SerializerMethodField()
    can_assign = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField(read_only=True)
    action_group = serializers.SerializerMethodField(read_only=True)
    current_officer = serializers.SerializerMethodField()

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'lodgement_date',
                'contact_details_id',     
                'fee_waiver_purpose',     
                #'visits',
                'processing_status',
                'proposed_status',
                'can_process',
                'can_assign',
                'assigned_officer',
                'assigned_officer_id',
                'action_group',
                'current_officer',
                #'comments_to_applicant',
                )
        read_only_fields = (
            'id',
            'lodgement_number',
            'lodgement_date',
        )

    def get_action_group(self, obj):
        return EmailUserSerializer(obj.relevant_access_group, many=True).data

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_proposed_status(self,obj):
        return obj.get_proposed_status_display()

    def get_can_process(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            elif user in obj.relevant_access_group:
                return True
        return False

    def get_can_assign(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if user in obj.relevant_access_group:
                return True
        return False

    def get_assigned_officer(self,obj):
        if obj.assigned_officer:
            return obj.assigned_officer.get_full_name()
        return None

    def get_current_officer(self,obj):
        request = self.context.get('request')
        if request:
            return {
                'id': self.context['request'].user.id,
                'name': self.context['request'].user.get_full_name(),
                'email': self.context['request'].user.email
            }


class FeeWaiverSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()
    contact_details_id = serializers.IntegerField(
            required=True, write_only=True, allow_null=False)
    processing_status = serializers.SerializerMethodField()
    proposed_status = serializers.SerializerMethodField()
    can_process = serializers.SerializerMethodField()
    can_assign = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField(read_only=True)
    action_group = serializers.SerializerMethodField(read_only=True)
    current_officer = serializers.SerializerMethodField()

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'lodgement_date',
                'contact_details_id',     
                'fee_waiver_purpose',     
                'visits',
                'processing_status',
                'proposed_status',
                'can_process',
                'can_assign',
                'assigned_officer',
                'assigned_officer_id',
                'action_group',
                'current_officer',
                'comments_to_applicant',
                )
        read_only_fields = (
            'id',
            'lodgement_number',
            'lodgement_date',
        )

    def get_action_group(self, obj):
        return EmailUserSerializer(obj.relevant_access_group, many=True).data

    def get_visits(self, obj):
        visits = []
        for visit in obj.visit.all():
            visits.append(FeeWaiverVisitSerializer(visit).data)
        return visits

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_proposed_status(self,obj):
        return obj.get_proposed_status_display()

    def get_can_process(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            elif user in obj.relevant_access_group:
                return True
        return False

    def get_can_assign(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if user in obj.relevant_access_group:
                return True
        return False

    def get_assigned_officer(self,obj):
        if obj.assigned_officer:
            return obj.assigned_officer.get_full_name()
        return None

    def get_current_officer(self,obj):
        request = self.context.get('request')
        if request:
            return {
                'id': self.context['request'].user.id,
                'name': self.context['request'].user.get_full_name(),
                'email': self.context['request'].user.email
            }


class FeeWaiverDTSerializer(serializers.ModelSerializer):
    contact_name = serializers.SerializerMethodField()
    processing_status = serializers.SerializerMethodField()
    proposed_status = serializers.SerializerMethodField()
    can_process = serializers.SerializerMethodField()
    action_shortcut = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField(read_only=True)
    latest_feewaiver_document = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    #licence_document = serializers.CharField(source='licence_document._file.url')

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'contact_name',
                'participants',
                #'contact_details',
                #'submitter',
                'processing_status',
                'proposed_status',
                #'lodgement_date',
                'lodgement_date',
                'can_process',
                'assigned_officer',
                'action_shortcut',
                'comments_to_applicant',
                'latest_feewaiver_document',
                #document,
                #assigned_to,
                )
        read_only_fields = (
            'id',
        )

    #def get_lodgement_date(self, obj):
     #   return obj.lodgement_date.strftime('%d/%m/%Y')
    def get_participants(self, obj):
        if obj.contact_details:
            return obj.contact_details.participants.name

    def get_assigned_officer(self,obj):
        if obj.assigned_officer:
            return obj.assigned_officer.get_full_name()
        return None

    def get_contact_name(self, obj):
        if obj.contact_details:
            return obj.contact_details.contact_name

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_proposed_status(self,obj):
        return obj.get_proposed_status_display()

    def get_can_process(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            elif user in obj.relevant_access_group:
                return True
        return False

    def get_action_shortcut(self, obj):
        #link = '<div v-if="show_spinner"><i class="fa fa-2x fa-spinner fa-spin"></i></div><div v-else>'
        link = ''
        if self.get_can_process(obj) and obj.processing_status == 'with_approver':
            if obj.proposed_status == 'issue':
                link +=  '<a href="{}" class="action-{}" data-issue="{}">Issue Fee Waiver</a><br/>'.format(obj.id, obj.id, obj.id)
            if obj.proposed_status == 'concession':
                #link +=  '<a href="#${full.id}" data-concession="${full.id}">Concession</a><br/>'
                link +=  '<a href="{}" class="action-{}" data-concession="{}">Issue Concession</a><br/>'.format(obj.id, obj.id, obj.id)
            if obj.proposed_status == 'decline':
                #link +=  '<a href="#${full.id}" data-decline="${full.id}">Decline</a><br/>'
                link +=  '<a href="{}" class="action-{}" data-decline="{}">Decline</a><br/>'.format(obj.id, obj.id, obj.id)
        #link += '</div>'
        return link

    def get_latest_feewaiver_document(self, obj):
        #url = ''
        #if obj.documents.order_by('-uploaded_date'):
        #    url = obj.documents.order_by('-uploaded_date')[0]._file.url
        #return url
        return obj.latest_feewaiver_document


class FeeWaiverDocSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()
    contact_name = serializers.SerializerMethodField()
    participants_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    contact_details = ContactDetailsSerializer()
    processing_status = serializers.SerializerMethodField()
    proposed_status = serializers.SerializerMethodField()
    can_process = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField()
    approver = serializers.SerializerMethodField()
    full_camping_waiver_exists = serializers.SerializerMethodField()
    part_camping_waiver_exists = serializers.SerializerMethodField()
    concession = serializers.SerializerMethodField()
    #licence_document = serializers.CharField(source='licence_document._file.url')

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'contact_name',
                'contact_details',
                #'submitter',
                'processing_status',
                'proposed_status',
                #'lodgement_date',
                'lodgement_date',
                'can_process',
                'assigned_officer',
                'approver',
                'comments_to_applicant',
                'visits',
                'address',
                'full_camping_waiver_exists',
                'part_camping_waiver_exists',
                'participants_name',
                'concession',
                #document,
                #assigned_to,
                )
        read_only_fields = (
            'id',
        )

    #def get_lodgement_date(self, obj):
     #   return obj.lodgement_date.strftime('%d/%m/%Y')

    def get_address(self, obj):
        return (obj.contact_details.postal_address + '\n' +
                obj.contact_details.suburb + '\n' +
                obj.contact_details.state + '\n' +
                obj.contact_details.postcode + '\n')

    def get_visits(self, obj):
        visits = []
        for visit in obj.visit.all():
            visits.append(FeeWaiverVisitSerializer(visit).data)
        return visits

    def get_full_camping_waiver_exists(self, obj):
        waiver_exists = False
        for visit in obj.visit.all():
            if visit.camping_assessment == 'full_waiver':
                waiver_exists = True
        return waiver_exists

    def get_part_camping_waiver_exists(self, obj):
        waiver_exists = False
        for visit in obj.visit.all():
            if visit.camping_assessment == 'child_rate':
                waiver_exists = True
        return waiver_exists

    def get_assigned_officer(self,obj):
        if obj.assigned_officer:
            return obj.assigned_officer.get_full_name()
        return None

    def get_approver(self,obj):
        request = self.context.get('request')
        if request:
            return request.user.get_full_name()
        return None

    def get_contact_name(self, obj):
        if obj.contact_details:
            return obj.contact_details.contact_name

    def get_participants_name(self, obj):
        if obj.contact_details and obj.contact_details.participants:
            return obj.contact_details.participants.name

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_proposed_status(self,obj):
        return obj.get_proposed_status_display()

    def get_can_process(self,obj):
        # Check if currently logged in user has access to process the proposal
        #import ipdb; ipdb.set_trace()
        request = self.context.get('request')
        if request:
            user = request.user
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            elif user in obj.relevant_access_group:
                return True
        return False

    def get_concession(self,obj):
        if obj.processing_status == 'concession':
            return True


class ParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        fields = (
                'id',
                'name',
                )
        read_only_fields = (
            'id',
        )


class TemporaryDocumentCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryDocumentCollection
        fields = ('id',)

