DELETE FROM public.power_weight;

DELETE FROM public.player;

DELETE FROM public.power;

ALTER SEQUENCE player_id_seq RESTART WITH 1;

ALTER SEQUENCE power_id_seq RESTART WITH 1;

INSERT INTO public.player(name)
VALUES ('Exits');

INSERT INTO public.player(name)
VALUES ('Possession');

INSERT INTO public.player(name)
VALUES ('Theory');

INSERT INTO public.player(name)
VALUES ('Iota');

INSERT INTO public.player(name)
VALUES ('Sentient');

INSERT INTO public.power(name, cooldown, on_use_function)
VALUES ('Basic Gun', 5, 'pwr_basic_gun_on_use');

INSERT INTO public.power(name, cooldown, on_use_function)
VALUES ('Cross Cannon', 30, 'pwr_cross_cannon_on_use');

INSERT INTO public.power(name, cooldown, on_use_function)
VALUES ('Body Slam', 30, 'pwr_body_slam_on_use');

INSERT INTO public.power(name, cooldown, on_use_function)
VALUES ('Laser', 200, 'pwr_laser_on_use');

INSERT INTO public.power(name, cooldown, on_use_function)
VALUES ('Bomb', 50, 'pwr_bomb_on_use');

INSERT INTO public.power_weight(player_id, power_id)
VALUES (1, 1);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (1, 2);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (2, 1);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (2, 2);