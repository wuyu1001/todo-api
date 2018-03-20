from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

class Admin(UserMixin, db.Model):
    """
    Create an admin table
    """

    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Admin: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class AccountInfo(db.Model):

    __tablename__ = 'account_info'

    id = db.Column(db.Integer, primary_key=True)
    TB_ID = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.String(128))
    end_time = db.Column(db.String(128))
    key = db.Column(db.String(128), unique=True)
    ImpDate = db.Column(db.String(200))


    def __repr__(self):
        return '{}, {}'.format(self.key, self.TB_ID,)
        
class Function(db.Model):
    
    __tablename__ = 'functions'
    
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.String(200))
    count = db.Column(db.String(200))
    adGroupId = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    itemLinkUrl = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    title = db.Column(db.String(200))
    campaignId = db.Column(db.String(200))
    token = db.Column(db.String(200))
    itemTitle = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    categoryId = db.Column(db.String(200))
    bidWordData = db.Column(db.Text)
    itemImgUrl = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class BidWord(db.Model):
    
    __tablename__ = 'bidword'
    
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.String(200))
    count = db.Column(db.String(200))
    adGroupId = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    itemLinkUrl = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    title = db.Column(db.String(200))
    campaignId = db.Column(db.String(200))
    token = db.Column(db.String(200))
    itemTitle = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    categoryId = db.Column(db.String(200))
    bidWordData = db.Column(db.Text)
    itemImgUrl = db.Column(db.String(200))
    ImpDate = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class BackUp(db.Model):
    
    __tablename__ = 'backup'
    
    id = db.Column(db.Integer, primary_key=True)
    adGroupId = db.Column(db.String(200))
    campaignId = db.Column(db.String(200))
    categoryId = db.Column(db.String(200))
    count = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    data = db.Column(db.Text)
    itemId = db.Column(db.String(200))
    itemImgUrl = db.Column(db.String(200))
    itemLinkUrl = db.Column(db.String(200))
    itemTitle = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    title = db.Column(db.String(200))
    token = db.Column(db.String(200))
    ImpDate = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class Back_Up(db.Model):
    
    __tablename__ = 'back_up'
    
    id = db.Column(db.Integer, primary_key=True)
    adGroupId = db.Column(db.String(200))
    campaignId = db.Column(db.String(200))
    categoryId = db.Column(db.String(200))
    count = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    data = db.Column(db.Text)
    itemId = db.Column(db.String(200))
    itemImgUrl = db.Column(db.Text)
    itemLinkUrl = db.Column(db.String(200))
    itemTitle = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    title = db.Column(db.String(200))
    token = db.Column(db.String(200))
    ImpDate = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)

class TaoKouLin(db.Model):
    
    __tablename__ = 'taokoulin'
    
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.String(200))
    fuserId = db.Column(db.String(200))
    adGroupId = db.Column(db.String(200))
    CategoryId = db.Column(db.String(200))
    md5 = db.Column(db.String(200))
    campaignId = db.Column(db.String(200))
    fmd5 = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    token = db.Column(db.String(200))
    userId = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class Manage(db.Model):
    
    __tablename__ = 'manage'
    
    id = db.Column(db.Integer, primary_key=True)
    Cnt = db.Column(db.String(200))
    Title = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    token = db.Column(db.String(200))
    ImpDate = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class Optimization(db.Model):
    
    __tablename__ = 'optimization'
    
    id = db.Column(db.Integer, primary_key=True)
    custId = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    ruleName = db.Column(db.String(200))
    ruleObject = db.Column(db.String(200))
    ruleRate = db.Column(db.String(200))
    ruleTime = db.Column(db.String(200))
    ruleTodo = db.Column(db.String(200))
    rules = db.Column(db.String(200))
    token = db.Column(db.String(200))
    
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        
class Control(db.Model):
    
    __tablename__ = 'control'
    
    id = db.Column(db.Integer, primary_key=True)
    creativeImgUrl_1 = db.Column(db.String(200))
    creativeImgUrl_2 = db.Column(db.String(200))
    creativeImgUrl_3 = db.Column(db.String(200))
    creativeImgUrl_4 = db.Column(db.String(200))
    creativeImgUrl_5 = db.Column(db.String(200))
    creativeImgUrl_reset = db.Column(db.String(200))
    creativeTitle = db.Column(db.String(200))
    custId = db.Column(db.String(200))
    endTime = db.Column(db.String(200))
    isCheckTime = db.Column(db.String(200))
    isDelCreative = db.Column(db.String(200))
    isQAdd = db.Column(db.String(200))
    maxPrice = db.Column(db.String(200))
    md5 = db.Column(db.String(200))
    nickName = db.Column(db.String(200))
    operName = db.Column(db.String(200))
    qWait = db.Column(db.String(200))
    startTime = db.Column(db.String(200))
    step = db.Column(db.String(200))
    token = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Function: {}>'.format(self.itemId)
        



