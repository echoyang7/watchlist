import click

from watchlist import app, db
from watchlist.models import User, Movie,Message

#执行 flask admin 命令，输入用户名和密码后，即可创建管理员账户。
@app.cli.command()
@click.option('--username',prompt=True,help='The username used to lohin')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login')
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username,name='Admin') #管理员默认名字Admin
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')

@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge_message(count):
    db.create_all()
    from faker import Faker

    fake = Faker()
    messages = [
        {'name': 'Amy', 'body': 'Wow!'},
        {'name': 'Shelton', 'body': 'WowWow!'},
        {'name': 'echo', 'body': 'Heihei!'},
    ]

    for m in range(count):
        message = Message(
            name=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)

    db.session.commit()
    click.echo('Done.')