from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)


offices = []
for i in range(1,11):
    offices.append({"number": i, "tenant": ""})


@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices, 
            'id': id
        }
    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '': 
                    return{
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        }, 
                        'id': id
                    }
                
                office['tenant'] = login 
                return{
                    'jsonrpc': '2.0',
                    'result': offices, 
                    'id': id
                }
            
    if data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        
        office_number = data['params']  
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office not booked'
                        }, 
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }      
                
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': offices, 
                    'id': id
                }    
    

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }


@lab6.route('/lab6/')
def lab():
    return render_template('/lab6/lab6.html')