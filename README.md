最近在github上发现一个可以用来自动帮你挂英雄联盟(除国服)电竞引擎(可以开出头像和表情)的项目,CapsuleFarmerEvolved,[github原项目链接](https://github.com/LeagueOfPoro/CapsuleFarmerEvolved)简单来说就是本来是通过看比赛获取奖励的,它帮助你进行观看.
对这个活动有兴趣的话,大家可以自行去官网看细节:[英雄联盟电竞](https://lolesports.com/)不过需要魔法才能访问.
***
当然,挂着躺拿奖励是好的,但是总觉得心里有点痒痒的,究竟什么时候收到drops呢,总要时不时查看一下.
后来发现这个项目本来就有可以链接**discord**的功能,但是众所周知,discord国内是不能访问的,那么我就想到了,反正都是使用**Webhook**的原理,那么何不用大家**最熟悉的钉钉**来推送奖励信息呢?
**经过一番计算机小白的摸索,终于实现了!**
***
本版本是在原项目的1.4版本下进行的修改,加入了对钉钉的支持和饭碗警告的支持
***
至于这个软件是怎么使用的我这里就不多说的,有兴趣的可以去github上看原作者的readme,非常详细,多个平台都可以运行/
***
## 钉钉配置
以下为对钉钉配置的过程:

首先在钉钉里创建一个群(什么群都可以啦,我这里为家校群),点击设置里的智能群助手,
![在这里插入图片描述](https://img-blog.csdnimg.cn/cdede24e49494f4fa8dc9cc42849bac9.png)
选择添加机器人
![在这里插入图片描述](https://img-blog.csdnimg.cn/c3593d17c85e4bfd9414ed50bfc75e85.png)

选择自定义机器人
![在这里插入图片描述](https://img-blog.csdnimg.cn/463e1dbcda9e48f6b5238c36efc16104.png)
然后安全设置中选择自定义关键词,输入Capsule(至于为什么要这样,因为其他两个选项都不太得劲嘿嘿)
![在这里插入图片描述](https://img-blog.csdnimg.cn/1107ec386a0c47c686603fa70afc50c8.png)
然后把这里出现的Webhook给复制下来(并且不要跟别人说哦)
![在这里插入图片描述](https://img-blog.csdnimg.cn/594a2cb32d484f5f925be20ec20ca3b2.png)
这样,一个机器人就出现在你的群里面了.
***
## 软件config.yaml配置
然后是CapsuleFarmerEvolved这个软件的配置问题啦.打开config.yaml文件(使用记事本就可以),然后在accounts的上面输入
connectorDropsUrl: "你的钉钉Webhook链接"
具体如下,
![在这里插入图片描述](https://img-blog.csdnimg.cn/25ec14d052ff4d1896bf1aa74e13764d.png)
一切就配置好了,你可以开始打开软件开始挂电竞引擎了.
![在这里插入图片描述](https://img-blog.csdnimg.cn/f901908ddde24dc0afecfc0092c8985c.png)
当收到Drops的时候会在你配置的钉钉群里提醒你的,如下图:(如有多个账号的话我设置成只会收到第一个账号的掉落信息)
![在这里插入图片描述](https://img-blog.csdnimg.cn/4414734066f94f249fb96f3e1a3ec6d2.png)
***
接下来是饭碗提醒部分:
打开饭碗提醒,添加转发规则,需要更改设置如下
![在这里插入图片描述](https://img-blog.csdnimg.cn/649fce48b13e46fc87878b678241c550.png)
设置好为下图所示:
![在这里插入图片描述](https://img-blog.csdnimg.cn/b21c22f17389497f8bfe38eeb19892ca.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/3b05137cd93c4f7db2d1f7b0fda5ea6c.png)
这里联系方式建议选择饭碗警告应用,因为前三个是收费的,第四个是需要魔法的.
至于联系方式的配置问题,自行在饭碗警告里根据流程配置.
之后和钉钉配置一样,在配置文件config.yaml中加入对应格式的webhook链接就可以了.

以下为TG中提醒的实例:
![在这里插入图片描述](https://img-blog.csdnimg.cn/6ee533317efc4250a7dcdc56843ae745.png)
***
***
新手上路,有错请指正;
