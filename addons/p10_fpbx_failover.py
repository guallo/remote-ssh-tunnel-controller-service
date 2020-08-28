import sys
import enum
import logging

from pydispatch import dispatcher

from fpbx_client_lib import fpbx_context

from rssht_controller_service import config
from rssht_controller_service.service import Service


logger = logging.getLogger(__name__)
conn_status = {}
call_flow_status = {}


class Signal(enum.Enum):
    SET_CALL_FLOW_STATUS = enum.auto()


def check_agent(agent, now):
    agent_id = agent.get_id()
    logger.debug('Checking agent %s.', agent_id)
    
    if agent_id not in config.AGENT_CLIENT_MAP:
        return
    
    client = config.AGENT_CLIENT_MAP[agent_id]
    update_conn_status(agent, now, client['switch-back-threshold'], client['switch-threshold'])
    agent_conn_status = conn_status[agent_id]
    
    if not (agent_conn_status['steady-up'] or agent_conn_status['steady-down']):
        return
    
    agent_call_flow_status = agent_conn_status['steady-up']
    
    if agent_id in call_flow_status and call_flow_status[agent_id] == agent_call_flow_status:
        return
    
    dispatcher.send(signal=Signal.SET_CALL_FLOW_STATUS, 
                    sender=sys.modules[check_agent.__module__], 
                    simulation=client['simulate'], agent=agent, 
                    base_url=client['base_url'], domain=client['domain'], 
                    call_flow=client['call_flow'], status=agent_call_flow_status)
    
    fpbx_set_call_flow_status(client['simulate'], client['base_url'], 
                                client['username'], client['password'], 
                                client['domain'], client['call_flow'], 
                                agent_call_flow_status)
    call_flow_status[agent_id] = agent_call_flow_status


def update_conn_status(agent, now, steady_up_threshold, steady_down_threshold):
    agent_id = agent.get_id()
    timedelta = now - agent.get_status().get_timestamp()
    conn_down = timedelta.total_seconds() > config.CONNECTION_DOWN_THRESHOLD
    
    if agent_id not in conn_status:
        conn_status[agent_id] = {
            'down': conn_down,
            'datetime': now,
            'steady-up': False,
            'steady-down': False
        }
    
    agent_conn_status = conn_status[agent_id]
    
    if agent_conn_status['down'] == conn_down:
        if agent_conn_status['datetime'] is not None:
            timedelta = now - agent_conn_status['datetime']
            
            if conn_down:
                if timedelta.total_seconds() > steady_down_threshold:
                    agent_conn_status['datetime'] = None
                    agent_conn_status['steady-up'] = False
                    agent_conn_status['steady-down'] = True
            else:
                if timedelta.total_seconds() > steady_up_threshold:
                    agent_conn_status['datetime'] = None
                    agent_conn_status['steady-up'] = True
                    agent_conn_status['steady-down'] = False
    else:
        agent_conn_status['down'] = conn_down
        
        if agent_conn_status['datetime'] is None:
            agent_conn_status['datetime'] = now
        else:
            if agent_conn_status['steady-up'] or agent_conn_status['steady-down']:
                agent_conn_status['datetime'] = None
            else:
                agent_conn_status['datetime'] = now


def fpbx_set_call_flow_status(simulate, base_url, username, password, domain, 
                                call_flow, status):
    logger.debug('%sUpdating call flow %s of domain %s, setting status %r.', 
                simulate and '[SIMULATION] ' or '', call_flow, domain, status)
    
    if simulate:
        return
    
    with fpbx_context.FPBXContext(base_url, config.GECKODRIVER_BIN, 
                                config.FIREFOX_BIN, config.BROWSER_HEADLESS, 
                                config.WEBDRIVER_TIMEOUT, 
                                config.GECKODRIVER_LOG_FILENAME, 
                                config.GECKODRIVER_LOG_LEVEL) as login_page:
        
        call_flow_edit_page = login_page.login(username, password) \
            .change_to_domain(domain) \
            .goto_call_flows() \
            .edit(call_flow)
        
        cur_status = call_flow_edit_page.get_values()['status']
        
        if cur_status != status:
            call_flow_edit_page.save(status=status).logout()
        else:
            logger.debug('Call flow %s of domain %s was already with status %r.', 
                call_flow, domain, status)
            call_flow_edit_page.logout()


dispatcher.connect(check_agent, signal=Service.Signal.CHECK_AGENT, sender=Service.instance)
