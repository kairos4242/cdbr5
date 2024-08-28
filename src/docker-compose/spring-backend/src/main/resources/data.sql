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

INSERT INTO public.power(name)
VALUES ('Pretend');

INSERT INTO public.power(name)
VALUES ('Ossify');

INSERT INTO public.power_weight(player_id, power_id)
VALUES (1, 1);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (1, 2);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (2, 1);

INSERT INTO public.power_weight(player_id, power_id)
VALUES (2, 2);