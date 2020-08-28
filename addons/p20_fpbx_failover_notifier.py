import ssl
import smtplib
import logging
import datetime
from email.message import EmailMessage

from pydispatch import dispatcher

from rssht_controller_service import config

from . import p10_fpbx_failover as fpbx_failover


logger = logging.getLogger(__name__)


def notify(signal, simulation, agent, base_url, domain, call_flow, status):
    if config.SKIP_FIRST_NOTIFICATION_ATTEMPT \
            and getattr(agent, 'first_notification_attempt', True):
        logger.debug('Skipping first notification attempt by email about '
                    'signal %r for agent %r, base url %r, domain %r, '
                    'call flow %r, status %r and simulation %r.', 
                    signal.name, agent.get_id(), base_url, domain, call_flow, 
                    status, simulation)
        agent.first_notification_attempt = False
        return
    
    logger.debug('Notifying by email about signal %r for agent %r, '
                'base url %r, domain %r, call flow %r, status %r and simulation %r.', 
                signal.name, agent.get_id(), base_url, domain, call_flow, status, 
                simulation)
    
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    local_time = utc_time.astimezone()
    
    template_kwargs = {
        'utc_time': utc_time, 
        'local_time': local_time, 
        'is_simulation': simulation and '[SIMULATION]' or '', 
        'agent': agent.get_id(), 
        'base_url': base_url, 
        'domain': domain, 
        'call_flow': call_flow, 
        'status': status, 
    }
    
    msg = EmailMessage()
    msg['From'] = config.EMAIL_FROM
    msg['To'] = ', '.join(config.EMAIL_TO)
    if status:
        msg['Subject'] = config.EMAIL_NORMAL_SUBJECT_TPL.format(**template_kwargs)
        msg.set_content(config.EMAIL_NORMAL_CONTENT_TPL.format(**template_kwargs))
    else:
        msg['Subject'] = config.EMAIL_FAILOVER_SUBJECT_TPL.format(**template_kwargs)
        msg.set_content(config.EMAIL_FAILOVER_CONTENT_TPL.format(**template_kwargs))

    with smtplib.SMTP(config.SMTP_ADDR, config.SMTP_PORT, timeout=config.TIMEOUT) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.send_message(msg)


dispatcher.connect(notify, signal=fpbx_failover.Signal.SET_CALL_FLOW_STATUS, sender=fpbx_failover)
