'''
说明：
  1. 对于使用ForeignKey引用的外部模型，on_delete建议还是设置为models.CASCADE。因为如果不删除，则处理模型时，需要对引用的外部模型不存在的异常做处理
  2. 鉴于以上原因，对于模型的操作，不建议提供真实的物理删除，都采用软删除的模式，仅将数据置为无效，不显示即可
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# hj_1_xxx: 用户级表
# hj_2_xxx: 用户扩展表

# 用户表
class User(models.Model):
    userUnionId = models.CharField(_('memUnionId'), max_length=64, null=True)
    userOpenId = models.CharField(_('userOpenId'), max_length=64, unique=True)  # 同一个账号下，仅有一个小程序的时候，不会返回UnionId，仅OpenId
    userNickName = models.CharField(_('memNickName'), max_length=64, null=True)  # 用户昵称
    userAvatarUrl = models.URLField(_('memAvatarUrl'), null=True)  # 用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表132*132正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
    userGender = models.CharField(_('memGender'), max_length=1, null=True)  # 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    userCity = models.CharField(_('memCity'), max_length=16, null=True)  # 用户所在城市
    userProvince = models.CharField(_('memProvince'), max_length=8, null=True)  # 用户所在省份
    userCountry = models.CharField(_('memCountry'), max_length=16, null=True)  # 用户所在国家
    userLanguage = models.CharField(_('memLanguage'), max_length=8, null=True)  # 用户的语言，简体中文为zh_CN
    userSessionCode = models.CharField(_('userSessionCode'), max_length=64, null=True)  # 用户最后一次有效的code
    userSessionKey = models.CharField(_('userSessionKey'), max_length=64, null=True)  # 用户最后一次有效的session_key
    userCreateTime = models.DateTimeField(_('memCreateTime'), auto_now_add=True)
    userLastModifyTime = models.DateTimeField(_('memLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_1_user'
        indexes = [
            models.Index(
                fields=['userUnionId'],
                name='userUnionId_idx',
            ),
            models.Index(
                fields=['userSessionCode'],
                name='userSessionCode_idx',
            ),
        ]

# 用户session表  -- 暂时未启用，登录的时候减少一次数据库操作，将code、key保存在User表中
class UserSession(models.Model):
    sessionOwner = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userOpenId')
    sessionCode = models.CharField(_('sessionCode'), max_length=64, null=True)
    sessionKey = models.URLField(_('sessionKey'), null=True)
    sessionCreateTime = models.DateTimeField(_('sessionCreateTime'), auto_now_add=True)
    sessionLastModifyTime = models.DateTimeField(_('sessionLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_2_usersession'
        indexes = [
            models.Index(
                fields=['sessionCode'],
                name='sessionCode_idx',
            ),
        ]

class Requirement(models.Model):
    reqTitle = models.CharField(_("reqTitle"), max_length=50)
    reqCreator = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userOpenId')
    reqDesc = models.CharField(_("reqDesc"), max_length=300)
    reqStatus = models.CharField(_("reqStatus"), max_length=10)  # Discussing -> Accept -> Developing -> Finished, Destroy-软删除标识
    reqRemark = models.CharField(_("reqRemark"), max_length=200)  # 自己用来做对需求的备注的
    reqCreateTime = models.DateTimeField(_("reqCreateTime"), auto_now_add=True)

    class Meta:
        db_table = 'hj_1_requirement'
        ordering = ['-reqCreateTime']

# 团队表
class Team(models.Model):
    teamName = models.CharField(_('teamName'), max_length=128)
    teamOwner = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userOpenId')  # User表不会删数据
    teamStatus = models.CharField(_('teamStatus'), default='inactive', max_length=8)  # 团队状态: Inactive, Active, Destroy
    teamDesc = models.CharField(_('teamDesc'), max_length=256)  # 团队描述
    teamNotice = models.CharField(_('teamNotice'), max_length=256)  # 团队公告
    teamCreateTime = models.DateTimeField(_('teamCreateTime'), auto_now_add=True)
    teamLastModifyTime = models.DateTimeField(_('teamLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_1_team'
        ordering = ['-teamCreateTime']
        indexes = [
            models.Index(
                fields=['teamName'],
                name='teamName_idx',
            ),
        ]

# 团队成员表(从用户授权后，调用wx.getUserInfo获取)
class TeamMember(models.Model):
    memTeamId = models.ForeignKey(Team, on_delete=models.CASCADE)  # Team表不会删数据，仅标记为destroy软删除
    memOpenId = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userOpenId')  # User表不会删数据，仅标记为destroy软删除
    memRole = models.CharField(_('memRole'), max_length=16)  # 用户在群中的角色：Manager-管理员，Owner-创建者/所有者， Member-成员
    memNickName = models.CharField(_('memNickName'), max_length=64)  # 群内昵称
    memJoinTime = models.DateTimeField(_('memJoinTime'), auto_now_add=True)
    memLastModifyTime = models.DateTimeField(_('memLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_1_teammember'
        indexes = [
            models.Index(
                fields=['memTeamId'],
                name='memTeamId_idx',
            ),
        ]


# 团队维度的费用汇总表
class TeamFee(models.Model):
    feeTeamId = models.ForeignKey(Team, on_delete=models.CASCADE)  # Team表不删数据，仅标记为destroy软删除
    feeName = models.CharField(_('feeName'), max_length=32)  # 该笔费用的名目，如：班费，活动经费，集资款等
    feeTotal = models.FloatField(_('feeTotal'))  # 这个字段没有用，只记录余额就够了
    feeRest = models.FloatField(_('feeRest'))
    feeCreateTime = models.DateTimeField(_('feeCreateTime'), auto_now_add=True)
    feeLastModifyTime = models.DateTimeField(_('feeLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_2_teamfee'

# 团队费用使用详情表
class TeamFeeDetail(models.Model):
    feeDetailTeamId = models.ForeignKey(Team, on_delete=models.CASCADE)  # Team表不删数据，仅标记为destroy软删除
    feeDetailItem = models.CharField(_('feeDetailItem'), max_length=64)
    feeDetailValue = models.FloatField(_('feeDetailValue'))
    feeDetailType = models.BooleanField(_('feeDetailType'))  # true: 收， false: 支
    feeDetailTax = models.CharField(_('feeDetailTax'), max_length=8)  # 票据类型：tax：发票， detail: 收据
    feeDetailTaxUrl = models.URLField(_('feeDetailTaxUrl'))  # 票据保存地址
    feeDetailTime = models.DateTimeField(_('feeDetailTime'))  # 费用发生时间
    feeDetailCreateTime = models.DateTimeField(_('feeDetailCreateTime'), auto_now_add=True)
    feeDetailLastModifyTime = models.DateTimeField(_('feeDetailLastModifyTime'), auto_now=True)

    class Meta:
        db_table = 'hj_2_teamfeedetail'