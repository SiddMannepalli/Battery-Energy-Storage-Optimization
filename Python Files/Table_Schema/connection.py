from db import engine, Session

class sessionManager:
    engine = engine
    Session = Session
    session = Session()