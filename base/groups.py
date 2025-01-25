def is_Admin(user):
    return user.groups.filter(name='Admin').exists()

def is_EventPlanner(user):
    return user.groups.filter(name='Event Planner').exists()

def is_Vendor(user):
    return user.groups.filter(name='Vendor').exists()

def is_Client(user):
    return user.groups.filter(name='Client').exists()