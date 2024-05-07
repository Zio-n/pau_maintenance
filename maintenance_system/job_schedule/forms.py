from django import forms
from .models import TaskFunnel
from accounts.models import User
from django.shortcuts import render, get_object_or_404
import uuid
import json
from django.core.mail import send_mail


DEPARTMENTS = [
         ('Electrical', 'Electrical'),
        ('Mechanical', 'Mechanical'),
        ('HVAC', 'HVAC'),
]

STATUS = [
        ('unassigned', 'unassigned'),
      ('assigned', 'assigned'),
      ('in progress', 'in progress'),
      ('completed', 'completed'),
]

PRIORITY = [
    ('High', 'High'),
      ('Mid', 'Mid'),
      ('Low', 'Low'),
]

BUILDING = [
    ('TYD', 'TYD'),
      ('SST', 'SST'),
      ('Museum', 'Museum'),
      ('Utility', 'Utility'),
      ('Other', 'Other'),
]

FLOORS = [
    ('Ground Floor', 'Ground Floor'),
      ('1st Floor', '1st Floor'),
      ('2nd Floor', '2nd Floor'),
      ('Other', 'Other'),
]

WINGS = [
    ('Wing A', 'Wing A'),
      ('Wing B', 'Wing B'),
      ('Executive Wing', 'Executive Wing'),
]

LOCATIONS = [
    ('Abakaliki', 'Abakaliki'),
    ('Abeokuta', 'Abeokuta'),
    ('Ado-Ekiti', 'Ado-Ekiti'),
    ('Akure', 'Akure'),
    ('Art and Graphics Studio', 'Art and Graphics Studio'),
    ('Asaba', 'Asaba'),
    ('ATM', 'ATM'),
    ('Audio-Visual Studio', 'Audio-Visual Studio'),
    ('Bauchi', 'Bauchi'),
    ('Benin', 'Benin'),
    ('Cafeteria', 'Cafeteria'),
    ('Central Store', 'Central Store'),
    ('Chapel', 'Chapel'),
    ('Chemistry lab', 'Chemistry lab'),
    ('Choir', 'Choir'),
    ('Clinic', 'Clinic'),
    ('Computer lab', 'Computer lab'),
    ('Control Room', 'Control Room'),
    ('Corridor', 'Corridor'),
    ('Creche', 'Creche'),
    ('Damaturu', 'Damaturu'),
    ('Data Centre', 'Data Centre'),
    ('Display room', 'Display room'),
    ('Electrical lab', 'Electrical lab'),
    ('Electronics lab', 'Electronics lab'),
    ('Eletrical Room', 'Eletrical Room'),
    ('Entrance', 'Entrance'),
    ('Enugu', 'Enugu'),
    ('ES1', 'ES1'),
    ('ES2', 'ES2'),
    ('ES3', 'ES3'),
    ('ES4', 'ES4'),
    ('Executive Cafeteria', 'Executive Cafeteria'),
    ('Executive Reception', 'Executive Reception'),
    ('Exhibition hall', 'Exhibition hall'),
    ('Foyer', 'Foyer'),
    ('Green Area', 'Green Area'),
    ('Ibadan', 'Ibadan'),
    ('ICT Office', 'ICT Office'),
    ('Ilorin', 'Ilorin'),
    ('Iroko', 'Iroko'),
    ('Jalingo', 'Jalingo'),
    ('Jos', 'Jos'),
    ('Kano', 'Kano'),
    ('Kitchen', 'Kitchen'),
    ('Lab Store', 'Lab Store'),
    ('Library', 'Library'),
    ('Lift', 'Lift'),
    ('Lobby', 'Lobby'),
    ('Lokoja', 'Lokoja'),
    ('Maiduguri', 'Maiduguri'),
    ('Meeting room', 'Meeting room'),
    ('Museum', 'Museum'),
    ('Newsroom', 'Newsroom'),
    ('Office', 'Office'),
    ('Open Area', 'Open Area'),
    ('Oshogbo', 'Oshogbo'),
    ('Owerri', 'Owerri'),
    ('Panel Room', 'Panel Room'),
    ('Panel\Facility Room', 'Panel\Facility Room'),
    ('Photography dark room', 'Photography dark room'),
    ('Port-Harcourt', 'Port-Harcourt'),
    ('Printing Room', 'Printing Room'),
    ('Radio Studio', 'Radio Studio'),
    ('Reception', 'Reception'),
    ('Restroom', 'Restroom'),
    ('RM001', 'RM001'),
    ('RM002', 'RM002'),
    ('RM003', 'RM003'),
    ('RM004', 'RM004'),
    ('RM005', 'RM005'),
    ('RM006', 'RM006'),
    ('RM007', 'RM007'),
    ('RM008', 'RM008'),
    ('RM101', 'RM101'),
    ('RM102', 'RM102'),
    ('RM201', 'RM201'),
    ('RM202', 'RM202'),
    ('RM203', 'RM203'),
    ('RM204', 'RM204'),
    ('RM205', 'RM205'),
    ('RM206', 'RM206'),
    ('RM207', 'RM207'),
    ('RM208', 'RM208'),
    ('RM209', 'RM209'),
    ('RM210', 'RM210'),
    ('RM211', 'RM211'),
    ('RM212', 'RM212'),
    ('RM214', 'RM214'),
    ('RM216', 'RM216'),
    ('RM218', 'RM218'),
    ('RM219', 'RM219'),
    ('RM220', 'RM220'),
    ('RM221', 'RM221'),
    ('RM222', 'RM222'),
    ('RM223', 'RM223'),
    ('RM224', 'RM224'),
    ('RM225', 'RM225'),
    ('RM226', 'RM226'),
    ('RM227', 'RM227'),
    ('RM228', 'RM228'),
    ('RM229', 'RM229'),
    ('RM230', 'RM230'),
    ('RM231', 'RM231'),
    ('RM232', 'RM232'),
    ('RM233', 'RM233'),
    ('RM234', 'RM234'),
    ('RM235', 'RM235'),
    ('RM237', 'RM237'),
    ('RM 238', 'RM 238'),
    ('RM239', 'RM239'),
    ('RM240', 'RM240'),
    ('RM241', 'RM241'),
    ('RM242', 'RM242'),
    ('RM243', 'RM243'),
    ('RM244', 'RM244'),
    ('RM246', 'RM246'),
    ('RM248', 'RM248'),
    ('RM249', 'RM249'),
    ('RM250', 'RM250'),
    ('RM251', 'RM251'),
    ('RM252', 'RM252'),
    ('RM253', 'RM253'),
    ('RM254', 'RM254'),
    ('RM255', 'RM255'),
    ('RM256', 'RM256'),
    ('Security', 'Security'),
    ('Services Office', 'Services Office'),
    ('Sit-Out', 'Sit-Out'),
    ('Sound Studio', 'Sound Studio'),
    ('SST Classroom 1', 'SST Classroom 1'),
    ('SST Classroom 2', 'SST Classroom 2'),
    ('SST Classroom 3', 'SST Classroom 3'),
    ('SST Classroom 4', 'SST Classroom 4'),
    ('SST Classroom 5', 'SST Classroom 5'),
    ('SST Classroom 6', 'SST Classroom 6'),
    ('Staff Room Store', 'Staff Room Store'),
    ('Student Affairs', 'Student Affairs'),
    ('Studio', 'Studio'),
    ('Study room', 'Study room'),
    ('Teccna', 'Teccna'),
    ('Terrace', 'Terrace'),
    ('Terrace Cafe', 'Terrace Cafe'),
    ('Thermofluid lab', 'Thermofluid lab'),
    ('Umuahia', 'Umuahia'),
    ('Utility', 'Utility'),
    ('Uyo', 'Uyo'),
    ('Yola', 'Yola'),
    ('Zaria', 'Zaria'),
    ('RM103', 'RM103'),
    ('RM104', 'RM104'),
    ('RM105', 'RM105'),
    ('RM106', 'RM106'),
    ('RM107', 'RM107'),
    ('RM108', 'RM108'),
    ('RM109', 'RM109'),
    ('RM110', 'RM110'),
    ('Other', 'Other'),
]

SERVICES = [
    ('A/C', 'A/C'),
    ('Electricity', 'Electricity'),
    ('Wood works', 'Wood works'),
    ('Plumbing', 'Plumbing'),
    ('Tiling', 'Tiling'),
    ('Aluminium works', 'Aluminium works'),
    ('Exteriors', 'Exteriors'),
    ('Painting', 'Painting'),
    ('Other', 'Other'),
]


class AddJobScheduleForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='add_job_schedule')
    task_dept = forms.ChoiceField(choices=DEPARTMENTS, required=True,)
    task_building = forms.ChoiceField(choices=BUILDING, required=True,)
    other_task_building = forms.CharField(required=False,)
    task_wing = forms.ChoiceField(choices=WINGS, required=True,)
    task_floor = forms.ChoiceField(choices=FLOORS, required=True,)
    other_task_floor = forms.CharField(required=False,)
    task_location = forms.ChoiceField(choices=LOCATIONS, required=True,)
    other_task_location = forms.CharField(required=False,)
    task_category = forms.ChoiceField(choices=SERVICES, required=True,)
    other_task_category = forms.CharField(required=False,)
    customer_name = forms.CharField(required=True,)
    customer_email = forms.CharField(required=True,)
    task_asset_with_fault = forms.CharField(required=True,)
    task_problem = forms.CharField(required=True,)
    task_fault_image = forms.FileField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_type'].widget.attrs.update({'id': 'id_add_action_type'})
        self.fields['task_building'].widget.attrs.update({'id': 'id_add_task_building'})
        self.fields['other_task_building'].widget.attrs.update({'id': 'id_add_other_task_building'})
        self.fields['task_location'].widget.attrs.update({'id': 'id_add_task_location'})
        self.fields['other_task_location'].widget.attrs.update({'id': 'id_add_other_task_location'})
        self.fields['task_wing'].widget.attrs.update({'id': 'id_task_wing'})
        self.fields['task_category'].widget.attrs.update({'id': 'id_add_task_category'})
        self.fields['other_task_category'].widget.attrs.update({'id': 'id_add_other_task_category'})        
        self.fields['task_asset_with_fault'].widget.attrs.update({'id': 'id_add_task_asset_with_fault'})
        self.fields['task_problem'].widget.attrs.update({'id': 'id_add_task_problem'})
        self.fields['task_note'].widget.attrs.update({'id': 'id_add_task_note'})
        self.fields['task_fault_image'].widget.attrs.update({'id': 'id_add_task_fault_image'})
        self.fields['task_floor'].widget.attrs.update({'id': 'id_add_task_floor'})
        self.fields['other_task_floor'].widget.attrs.update({'id': 'id_add_other_task_floor'})        
        self.fields['task_dept'].widget.attrs.update({'id': 'id_add_task_dept'})
        self.fields['customer_name'].widget.attrs.update({'id': 'id_add_customer_name'})
        self.fields['customer_email'].widget.attrs.update({'id': 'id_add_customer_email'})
        self.fields['scheduled_datetime'].widget.attrs.update({'id': 'id_add_scheduled_datetime'})   
                
    
    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name
    
    class Meta:
        model = TaskFunnel
        fields = ('task_dept', 'task_building', 'task_location', 'task_wing', 'task_category', 'task_asset_with_fault', 'task_problem', 'task_note', 'task_fault_image', 'task_floor', 'customer_name', 'customer_email', 'scheduled_datetime',)
        widgets = {
            'task_problem': forms.Textarea(attrs={'rows':'3'}),
            'task_note': forms.Textarea(attrs={'rows':'3'})
        }
    
    def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('task_building') == 'Other' and not cleaned_data.get('other_task_building'):
                self.add_error('other_task_building', "Please specify the other building.")
            if cleaned_data.get('task_floor') == 'Other' and not cleaned_data.get('other_task_floor'):
                self.add_error('other_task_floor', "Please specify the other floor.")
            if cleaned_data.get('task_location') == 'Other' and not cleaned_data.get('other_task_location'):
                self.add_error('other_task_location', "Please specify the other location.")
            if cleaned_data.get('task_category') == 'Other' and not cleaned_data.get('other_task_category'):
                self.add_error('other_task_category', "Please specify the other category.")
            return cleaned_data
    
    def clean_task_fault_image(self):
        fault_image = self.cleaned_data['task_fault_image']
        if fault_image:
            # Validate file type
            allowed_types = ['application/msword', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'audio/mpeg']
            if fault_image.content_type not in allowed_types:
                raise forms.ValidationError("Unsupported file type.")
            
            # Validate file size
            max_size = 10 * 1024 * 1024  # 10MB
            if fault_image.size > max_size:
                raise forms.ValidationError("File size exceeds the limit.")
            
            # Validate number of files
            if len(self.files.getlist('task_fault_image')) > 1:
                raise forms.ValidationError("Only one file is allowed.")
        return fault_image
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.form_id:
            instance.form_id = uuid.uuid4().hex
        if commit:
            instance.save()
        return instance



class UpdateTaskForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='update_task_schedule')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician', required=False,)
    task_dept = forms.ChoiceField(choices=DEPARTMENTS, required=True,)
    job_status = forms.ChoiceField(choices=STATUS, required=True,)
    priority_level = forms.ChoiceField(choices=PRIORITY, required=True,)
    update_task_id = forms.CharField(widget=forms.HiddenInput())
    fault_image_name = forms.CharField(required=False,)
    customer_name = forms.CharField(required=True,)
    customer_email = forms.CharField(required=True,)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_type'].widget.attrs.update({'id': 'id_edittask_action_type'})
        self.fields['update_task_id'].widget.attrs.update({'id': 'id_edittask_update_task_id'})
        self.fields['assigned_staff_id'].widget.attrs.update({'id': 'id_edittask_assigned_staff_id'})
        self.fields['job_status'].widget.attrs.update({'id': 'id_edittask_job_status'})
        self.fields['task_building'].widget.attrs.update({'id': 'id_edittask_task_building'})
        self.fields['task_location'].widget.attrs.update({'id': 'id_edittask_task_location'})
        self.fields['task_wing'].widget.attrs.update({'id': 'id_edittask_wing'})
        self.fields['task_category'].widget.attrs.update({'id': 'id_edittask_task_category'})
        self.fields['task_asset_with_fault'].widget.attrs.update({'id': 'id_edittask_asset_with_fault'})
        self.fields['task_problem'].widget.attrs.update({'id': 'id_edittask_task_problem'})
        self.fields['task_note'].widget.attrs.update({'id': 'id_edittask_task_note'})
        # self.fields['fault_image_name'].widget.attrs.update({'id': 'id_edittask_task_fault_image_name'})
        self.fields['task_floor'].widget.attrs.update({'id': 'id_edittask_task_floor'})
        self.fields['task_dept'].widget.attrs.update({'id': 'id_edittask_task_dept'})
        self.fields['customer_name'].widget.attrs.update({'id': 'id_edittask_customer_name'})
        self.fields['customer_email'].widget.attrs.update({'id': 'id_edittask_customer_email'})
        self.fields['scheduled_datetime'].widget.attrs.update({'id': 'id_edittask_scheduled_datetime'})        
        self.fields['priority_level'].widget.attrs.update({'id': 'id_edittask_priority_level'})
                
        self.fields['assigned_staff_id'].label_from_instance = self.label_from_instance
    
    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name
    
    class Meta:
        model = TaskFunnel
        fields = ('assigned_staff_id', 'job_status', 'task_dept', 'task_building', 'task_location', 'task_wing', 'task_category', 'task_asset_with_fault', 'task_problem', 'task_note', 'task_floor', 'customer_name', 'customer_email', 'scheduled_datetime', 'priority_level',)
        widgets = {
            'task_problem': forms.Textarea(attrs={'rows':'3'}),
            'task_note': forms.Textarea(attrs={'rows':'3'})
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class UpdateJobScheduleForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='update_job_schedule')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician', required=False,)
    task_dept = forms.ChoiceField(choices=DEPARTMENTS, required=True,)
    job_status = forms.ChoiceField(choices=STATUS, required=True,)
    priority_level = forms.ChoiceField(choices=PRIORITY, required=True,)
    update_job_id = forms.CharField(widget=forms.HiddenInput())
    fault_image_name = forms.CharField(required=False,)
    customer_name = forms.CharField(required=True,)
    customer_email = forms.CharField(required=True,)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_type'].widget.attrs.update({'id': 'id_edit_action_type'})
        self.fields['update_job_id'].widget.attrs.update({'id': 'id_edit_update_job_id'})
        self.fields['assigned_staff_id'].widget.attrs.update({'id': 'id_edit_assigned_staff_id'})
        self.fields['job_status'].widget.attrs.update({'id': 'id_edit_job_status'})
        self.fields['task_building'].widget.attrs.update({'id': 'id_edit_task_building'})
        self.fields['task_location'].widget.attrs.update({'id': 'id_edit_task_location'})
        self.fields['task_wing'].widget.attrs.update({'id': 'id_task_wing'})
        self.fields['task_category'].widget.attrs.update({'id': 'id_edit_task_category'})
        self.fields['task_asset_with_fault'].widget.attrs.update({'id': 'id_edit_task_asset_with_fault'})
        self.fields['task_problem'].widget.attrs.update({'id': 'id_edit_task_problem'})
        self.fields['task_note'].widget.attrs.update({'id': 'id_edit_task_note'})
        self.fields['fault_image_name'].widget.attrs.update({'id': 'id_edit_task_fault_image_name'})
        self.fields['task_floor'].widget.attrs.update({'id': 'id_edit_task_floor'})
        self.fields['task_dept'].widget.attrs.update({'id': 'id_edit_task_dept'})
        self.fields['customer_name'].widget.attrs.update({'id': 'id_edit_customer_name'})
        self.fields['customer_email'].widget.attrs.update({'id': 'id_edit_customer_email'})
        self.fields['scheduled_datetime'].widget.attrs.update({'id': 'id_edit_scheduled_datetime'})        
        self.fields['priority_level'].widget.attrs.update({'id': 'id_edit_priority_level'})
                
        self.fields['assigned_staff_id'].label_from_instance = self.label_from_instance
    
    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name
    
    class Meta:
        model = TaskFunnel
        fields = ('assigned_staff_id', 'job_status', 'task_dept', 'task_building', 'task_location', 'task_wing', 'task_category', 'task_asset_with_fault', 'task_problem', 'task_note', 'task_floor', 'customer_name', 'customer_email', 'scheduled_datetime', 'priority_level',)
        widgets = {
            'task_problem': forms.Textarea(attrs={'rows':'3'}),
            'task_note': forms.Textarea(attrs={'rows':'3'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        task_dept = cleaned_data.get('task_dept')
        assigned_staff = cleaned_data.get('assigned_staff_id')
        job_id = cleaned_data.get('update_job_id')
        job = get_object_or_404(TaskFunnel, pk=job_id)
        current_task_dept = job.task_dept
        current_assigned_staff = job.assigned_staff_id
        # Check if the department is changed
        if self.is_valid():
            # handle department
            if task_dept != current_task_dept:
                # Define the roles to be checked for each department
                department_roles = {
                    'Electrical': ['Team Lead Elect', 'Manager Elect', 'Ass Manager Elect'],
                    'Mechanical': ['Team Lead Mech', 'Manager Mech', 'Ass Manager Mech'],
                    'HVAC': ['Team Lead HVAC', 'Manager HVAC', 'Ass Manager HVAC'],
                }
                # Get users with roles corresponding to the selected department
                users_emails = []
                for role in department_roles.get(task_dept, []):
                    users = User.objects.filter(staff__role=role)
                    users_emails.extend(users.values_list('email', flat=True))
                print(f"user emails list {users_emails}")
                # Send emails to the collected users
                # send_mail(
                #     'Department Update',
                #     f'The department has been updated to {task_dept}',
                #     'from@example.com',
                #     users_emails,
                #     fail_silently=True,
                # )
            # handle assigned user
            if assigned_staff != current_assigned_staff:
                newly_assigned_email = assigned_staff.email
                print(f"Sending email to {newly_assigned_email} for assignment")
                # send_mail(
                #     'Assignment Update',
                #     f'You have been assigned a new task.',
                #     'from@example.com',
                #     [newly_assigned_email],
                #     fail_silently=True,
                # )
            
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
