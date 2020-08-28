from rssht_controller_service import config

# True or False
config.SKIP_FIRST_NOTIFICATION_ATTEMPT = False

# Domain name of SMTP server
config.SMTP_ADDR = 'mail.mydomain.com'
# Port for STARTTLS
config.SMTP_PORT = 587
# Full email address
config.SMTP_USERNAME = 'username@mydomain.com'
config.SMTP_PASSWORD = 'password'

# Full email address
config.EMAIL_FROM = 'username@mydomain.com'
# List of recipients' full email addresses
config.EMAIL_TO = ['someone@somedomain.com', 'anotherone@anotheronedomain.com']

# Email notification template for when entering the failover state.
# The following template variables are available:
#     {utc_time} the notification time in UTC timezone.
#     {local_time} the notification time in the system local timezone.
#     {is_simulation} indicates if it is a simulation or real. Can be '[SIMULATION]' or '' (empty string).
#     {agent} the Agent's ID.
#     {base_url} the FusionPBX's Base URL.
#     {domain} the Domain's name.
#     {call_flow} the Call Flow's name.
#     {status} the new Call Flow's Status, that can be True or False.
config.EMAIL_FAILOVER_SUBJECT_TPL = '{is_simulation} {domain} is entering in failover state'
config.EMAIL_FAILOVER_CONTENT_TPL = '''\
{is_simulation} {domain} is entering in failover state.

Notification Time: {local_time:%m-%d-%Y %I:%M:%S %p}
Agent ID: {agent}
FusionPBX Base URL: {base_url}
Call Flow Name: {call_flow}
Call Flow Status: {status}
'''

# Email notification template for when returning to normal state.
# The following template variables are available:
#     {utc_time} the notification time in UTC timezone.
#     {local_time} the notification time in the system local timezone.
#     {is_simulation} indicates if it is a simulation or real. Can be '[SIMULATION]' or '' (empty string).
#     {agent} the Agent's ID.
#     {base_url} the FusionPBX's Base URL.
#     {domain} the Domain's name.
#     {call_flow} the Call Flow's name.
#     {status} the new Call Flow's Status, that can be True or False.
config.EMAIL_NORMAL_SUBJECT_TPL = '{is_simulation} {domain} is returning to normal state'
config.EMAIL_NORMAL_CONTENT_TPL = '''\
{is_simulation} {domain} is returning to normal state.

Notification Time: {local_time:%m-%d-%Y %I:%M:%S %p}
Agent ID: {agent}
FusionPBX Base URL: {base_url}
Call Flow Name: {call_flow}
Call Flow Status: {status}
'''
