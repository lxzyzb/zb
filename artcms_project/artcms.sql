create table if not exists user(
    id int unsigned not null auto_increment key comment "主键id",
    name varchar(20) not null comment "帐号",
    pwd varchar(100) not null comment "密码",
    addtime datetime not null comment "注册时间"

)engine=InnoDB default charset utf8 comment "会员";


create table if not exists art(
    id int unsigned not null auto_increment key comment "主键id",
    title varchar(100) not null comment "标题",
    cate tinyint(100) unsigned not null comment "密码",
    user_id int unsigned not null comment "作者",
    logo varchar(100) not null comment "封面",
    content mediumtext not null comment "文章",
    addtime datetime not null comment "发布时间"

)engine=InnoDB default charset=utf8 comment "文章";