import flask, forms, netmiko

app = flask.Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
        return flask.render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
#call form for inputting login info
   form = forms.signin()
   if form.validate_on_submit():
       data = {'username': form.username.data, 'password': form.password.data, 'ip_address': form.ip_address.data}
       #store login info in a session cookie
       flask.session['login'] = data
       # return to index page
       return flask.redirect('/')
   return flask.render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #delete session info
    flask.session.pop('login')
    return flask.redirect('/login')

@app.route('/helloworld')
def helloworld():
    # check for existence of session
    s = flask.session.get('login')
    #    set login info from session as dictionary
    session_info = {'device_type': "linux", 'ip': s['ip_address'], 'username': s['username'], 'password': s['password']}

    # initiate connection
    net_connect = netmiko.ConnectHandler(**session_info)
    #run command on remote host
    output = net_connect.send_command(
        "echo Hello World")
        #display command output
    return f'''
        <html>
            <body>
            <p> <pre>{output}</pre> </p>
            </body>
        </html>
    '''

@app.route('/ls')
def remote_ls():
    # check for existence of session
    s = flask.session.get('login')
    #    set login info from session as dictionary
    session_info = {'device_type': "linux", 'ip': s['ip_address'], 'username': s['username'], 'password': s['password']}

    # initiate connection
    net_connect = netmiko.ConnectHandler(**session_info)
    #run command on remote host
    output = net_connect.send_command(
        "ls")
        #display command output
    return f'''
        <html>
            <body>
            <p> {output} </p>
            </body>
        </html>
    '''