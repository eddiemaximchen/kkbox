create database kkbox;
use kkbox;

create table boards(id varchar(100) unique not null, title varchar(100) not null, img_url varchar(200));
create table charts(id int auto_increment primary key, board_id varchar(100) not null,song_name varchar(200) not null, song_url varchar(200) not null);
create table hits(id int auto_increment primary key, board_url varchar(100), song_url varchar(100),hit_time timestamp default NOW()); 

select * from boards order by id;
select boards.title as title, song_name, song_url from charts join boards on charts.board_id=boards.id;

select * from charts;
select * from boards;
select * from users;
select * from playlist;
SELECT * FROM hits;


select boards.id,boards.title as title, song_name, song_url from charts join boards on charts.board_id=boards.id order by charts.board_id;
select * from boards;

select count(*) as counts, charts.song_name as name from charts join hits on hits.song_url=charts.song_url group by charts.song_name order by count(*) desc limit 10