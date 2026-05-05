--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
d1b5b0c60a0f
\.


--
-- Data for Name: cancellation_policy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cancellation_policy (id, name, hours_before, penalty_percent) FROM stdin;
\.


--
-- Data for Name: hotels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hotels (id, name, city, address, stars, description, rating_sum, rating_count, policy_id) FROM stdin;
1	Esentai Royal	Almaty	╨Р╨╗╤М-╨д╨░╤А╨░╨▒╨╕ 77/7	5	╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡ ╤Б╨╛╨╖╨┤╨░╨╜╨╛ ╨░╨▓╤В╨╛╨╝╨░╤В╨╕╤З╨╡╤Б╨║╨╕ ╨┐╤А╨╕ ╤Б╨╕╨┤╨╕╨╜╨│╨╡.	20.00	5	\N
2	Astana Garden	Astana	╨Ь╨░╨╜╨│╨╕╨╗╨╕╨║ ╨Х╨╗ 10	4	╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡ ╤Б╨╛╨╖╨┤╨░╨╜╨╛ ╨░╨▓╤В╨╛╨╝╨░╤В╨╕╤З╨╡╤Б╨║╨╕ ╨┐╤А╨╕ ╤Б╨╕╨┤╨╕╨╜╨│╨╡.	40.00	10	\N
3	Shymkent Plaza Hotel	Shymkent	╨┐╤А. ╨в╨░╤Г╨║╨╡ ╨е╨░╨╜╨░	4	╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡ ╤Б╨╛╨╖╨┤╨░╨╜╨╛ ╨░╨▓╤В╨╛╨╝╨░╤В╨╕╤З╨╡╤Б╨║╨╕ ╨┐╤А╨╕ ╤Б╨╕╨┤╨╕╨╜╨│╨╡.	49.00	12	\N
4	Caspian Star	Aktau	15-╨╣ ╨╝╨╕╨║╤А╨╛╤А╨░╨╣╨╛╨╜	5	╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡ ╤Б╨╛╨╖╨┤╨░╨╜╨╛ ╨░╨▓╤В╨╛╨╝╨░╤В╨╕╤З╨╡╤Б╨║╨╕ ╨┐╤А╨╕ ╤Б╨╕╨┤╨╕╨╜╨│╨╡.	43.00	11	\N
5	Medeu Camp	Almaty	╨У╨╛╤А╨╜╨░╤П 465	3	╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡ ╤Б╨╛╨╖╨┤╨░╨╜╨╛ ╨░╨▓╤В╨╛╨╝╨░╤В╨╕╤З╨╡╤Б╨║╨╕ ╨┐╤А╨╕ ╤Б╨╕╨┤╨╕╨╜╨│╨╡.	31.00	8	\N
\.


--
-- Data for Name: room_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room_types (id, type_name, description) FROM stdin;
6	deluxe	as
7	family	sasa
8	general	sasa
9	president	sasa
10	suite	kuka
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, h_id, room_number, r_t_id, capacity, price_per_day, floor, description) FROM stdin;
1	1	101	9	4	78291.00	6	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
2	1	102	8	4	40255.00	12	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
3	1	103	8	2	21088.00	1	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
4	1	104	7	3	50145.00	11	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
5	1	105	10	3	13465.00	10	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
6	2	201	7	1	48186.00	5	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
7	2	202	10	2	12467.00	2	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
8	2	203	9	1	84320.00	11	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
9	2	204	10	3	46209.00	4	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
10	2	205	10	4	90710.00	10	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
11	3	301	10	2	18162.00	12	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
12	3	302	6	1	15788.00	5	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
13	3	303	7	4	53946.00	1	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
14	3	304	7	3	82527.00	8	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
15	3	305	10	2	27383.00	9	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
16	4	401	8	3	74783.00	1	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
17	4	402	9	3	45804.00	5	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
18	4	403	7	4	77733.00	9	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
19	4	404	7	4	52311.00	8	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
20	4	405	9	4	88972.00	9	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
21	5	501	6	1	28930.00	12	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
22	5	502	7	3	54884.00	9	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
23	5	503	10	1	26119.00	4	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
24	5	504	9	3	42352.00	9	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
25	5	505	9	1	58377.00	1	╨Ъ╨╛╨╝╤Д╨╛╤А╤В╨░╨▒╨╡╨╗╤М╨╜╤Л╨╣ ╨╜╨╛╨╝╨╡╤А ╤Б╨╛ ╨▓╤Б╨╡╨╝╨╕ ╤Г╨┤╨╛╨▒╤Б╤В╨▓╨░╨╝╨╕.
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role, is_active) FROM stdin;
13	beka	beka@mail.ru	$2b$12$RreRuiSI5nAgrCNaXTdASebXUwjoYn1ccNdOTFSEQQuawP.8yT/Qq	USER	t
14	Alikhan Kurman	alitop01@gmail.com	$2b$12$x2gDrofJr41Pj9INCnWzauufzHF1QuxwJGWjy8DUR0tytcSFatAA.	USER	t
15	TESTONG	test@test.com	$2b$12$oJOIUdy438jNj16NI.mZu.m3aUdWsDU3dNSmyKs.qe3c74Lfi/I3W	USER	t
16	Test User	test@example.com	$2b$12$bxzWa1D7Uu4QlPhpno25WuSTdScl.UVaCFh.dq4Uve6asDzYoAn/G	USER	t
17	limbo	limbo@mail.ru	$2b$12$4BP1Lz8ES3le78/poR903uvxSE5Nxxcx3ggY3I9iz4J27DGCppc.2	USER	t
19	Kuanysh Kurmanov	gamedagger6@gmail.com	$2b$12$Rq38v4hmJCWuMj69RmM/yev9qhJdWtt20qmd2lQ8YHPjTXmD.ecZq	ADMIN	t
20	HOPEBTW	hope@hope.com	$2b$12$R/xpvF9HETP.AKjfpdfifeoOeMj1ht7o.ANSAYHlEmHwffcyFBhI6	USER	t
22	Super Admin	sadmin@sadmin.com	$2b$12$qA7HnmqiNRGgIpjWSyossO8M1UX5d6/lbr.mwJoDaXABgjUD4huei	S-ADMIN	t
23	Jond Doe	johndoe@gmail.com	$2b$12$T52Fra7LinFfXsLDWmRj1eOBewHVYds3A0n5Zm.2FgNvKxi9xx0Gy	USER	t
18	Admin Kuka	admin@admin.com	$2b$12$lQTRyxLZlfWgLoQWlhwEsOgahoAUsXmcgo485ZkBAaiMd57CB91Zq	ADMIN	t
24	Test User	test@example1.com	$2b$12$2UEQQjRitTUtTsvIDkbH0OqlfiMwDihTMFUfrhUix4.53fvW9t4xi	USER	t
25	Beksultan Sauytbek	bekalek4ik1@gmail.com	$2b$12$1UC3tz.awcubZ3BNuWVZYeMsDWNHYNSJSNKOpOKtvRAkAQczXnNK2	USER	t
\.


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, r_id, check_in, check_out, status, user_id, total_price, created_at, cancelled_at, guest_count) FROM stdin;
1	19	2026-03-11 18:20:45.844112	2026-03-16 18:20:45.844112	confirmed	13	104622.00	2026-04-26 19:20:45.835693	\N	3
2	23	2026-04-09 18:20:45.847431	2026-04-14 18:20:45.847431	confirmed	13	52238.00	2026-04-26 19:20:45.835693	\N	1
3	13	2026-04-01 18:20:45.855393	2026-04-06 18:20:45.855393	confirmed	13	107892.00	2026-04-26 19:20:45.835693	\N	2
4	24	2026-03-18 18:20:45.856978	2026-03-20 18:20:45.856978	confirmed	13	84704.00	2026-04-26 19:20:45.835693	\N	3
5	11	2026-03-13 18:20:45.858389	2026-03-17 18:20:45.858389	confirmed	14	36324.00	2026-04-26 19:20:45.835693	\N	1
6	15	2026-03-04 18:20:45.859995	2026-03-08 18:20:45.859995	confirmed	14	54766.00	2026-04-26 19:20:45.835693	\N	2
7	15	2026-03-02 18:20:45.861867	2026-03-03 18:20:45.861867	confirmed	14	54766.00	2026-04-26 19:20:45.835693	\N	1
8	23	2026-03-27 18:20:45.863319	2026-03-28 18:20:45.863319	confirmed	15	52238.00	2026-04-26 19:20:45.835693	\N	1
9	9	2026-03-18 18:20:45.864622	2026-03-21 18:20:45.864622	confirmed	15	92418.00	2026-04-26 19:20:45.835693	\N	2
10	12	2026-04-16 18:20:45.865862	2026-04-17 18:20:45.865862	confirmed	15	31576.00	2026-04-26 19:20:45.835693	\N	1
11	15	2026-03-30 18:20:45.867088	2026-04-01 18:20:45.867088	confirmed	16	54766.00	2026-04-26 19:20:45.835693	\N	2
12	20	2026-04-07 18:20:45.8683	2026-04-11 18:20:45.8683	confirmed	16	177944.00	2026-04-26 19:20:45.835693	\N	2
13	22	2026-04-03 18:20:45.869516	2026-04-08 18:20:45.869516	confirmed	16	109768.00	2026-04-26 19:20:45.835693	\N	2
14	15	2026-04-09 18:20:45.87074	2026-04-14 18:20:45.87074	confirmed	16	54766.00	2026-04-26 19:20:45.835693	\N	1
15	13	2026-03-26 18:20:45.871959	2026-03-29 18:20:45.871959	confirmed	17	107892.00	2026-04-26 19:20:45.835693	\N	2
16	10	2026-03-02 18:20:45.87319	2026-03-03 18:20:45.87319	confirmed	17	181420.00	2026-04-26 19:20:45.835693	\N	4
17	24	2026-02-26 18:20:45.874386	2026-02-27 18:20:45.874386	confirmed	17	84704.00	2026-04-26 19:20:45.835693	\N	1
18	9	2026-03-12 18:20:45.875635	2026-03-13 18:20:45.875635	confirmed	18	92418.00	2026-04-26 19:20:45.835693	\N	3
19	9	2026-03-15 18:20:45.876885	2026-03-19 18:20:45.876885	confirmed	18	92418.00	2026-04-26 19:20:45.835693	\N	3
20	19	2026-03-22 18:20:45.878086	2026-03-27 18:20:45.878086	confirmed	18	104622.00	2026-04-26 19:20:45.835693	\N	1
21	15	2026-04-15 18:20:45.879284	2026-04-16 18:20:45.879284	confirmed	18	54766.00	2026-04-26 19:20:45.835693	\N	1
22	19	2026-03-30 18:20:45.88047	2026-03-31 18:20:45.88047	confirmed	19	104622.00	2026-04-26 19:20:45.835693	\N	2
23	6	2026-04-12 18:20:45.881673	2026-04-16 18:20:45.881673	confirmed	19	96372.00	2026-04-26 19:20:45.835693	\N	1
24	21	2026-04-12 18:20:45.882881	2026-04-15 18:20:45.882881	confirmed	19	57860.00	2026-04-26 19:20:45.835693	\N	1
25	19	2026-04-07 18:20:45.884068	2026-04-09 18:20:45.884068	confirmed	19	104622.00	2026-04-26 19:20:45.835693	\N	3
26	18	2026-04-02 18:20:45.885265	2026-04-07 18:20:45.885265	confirmed	19	155466.00	2026-04-26 19:20:45.835693	\N	1
27	17	2026-04-01 18:20:45.886455	2026-04-03 18:20:45.886455	confirmed	20	91608.00	2026-04-26 19:20:45.835693	\N	3
28	3	2026-03-24 18:20:45.8877	2026-03-25 18:20:45.8877	confirmed	20	42176.00	2026-04-26 19:20:45.835693	\N	1
29	5	2026-04-20 18:20:45.888907	2026-04-25 18:20:45.888907	confirmed	20	26930.00	2026-04-26 19:20:45.835693	\N	1
30	2	2026-04-12 18:20:45.890089	2026-04-16 18:20:45.890089	confirmed	20	80510.00	2026-04-26 19:20:45.835693	\N	4
31	6	2026-03-28 18:20:45.891685	2026-04-01 18:20:45.891685	confirmed	20	96372.00	2026-04-26 19:20:45.835693	\N	1
32	7	2026-04-04 18:20:45.893042	2026-04-08 18:20:45.893042	confirmed	22	24934.00	2026-04-26 19:20:45.835693	\N	2
33	9	2026-03-07 18:20:45.89464	2026-03-09 18:20:45.89464	confirmed	22	92418.00	2026-04-26 19:20:45.835693	\N	2
34	12	2026-03-07 18:20:45.896008	2026-03-08 18:20:45.896008	confirmed	22	31576.00	2026-04-26 19:20:45.835693	\N	1
35	20	2026-04-10 18:20:45.897353	2026-04-11 18:20:45.897353	confirmed	22	177944.00	2026-04-26 19:20:45.835693	\N	3
36	12	2026-03-29 18:20:45.898673	2026-04-02 18:20:45.898673	confirmed	23	31576.00	2026-04-26 19:20:45.835693	\N	1
37	1	2026-03-18 18:20:45.899942	2026-03-23 18:20:45.899942	confirmed	23	156582.00	2026-04-26 19:20:45.835693	\N	2
38	18	2026-03-02 18:20:45.901132	2026-03-03 18:20:45.901132	confirmed	23	155466.00	2026-04-26 19:20:45.835693	\N	4
39	19	2026-03-15 18:20:45.902316	2026-03-19 18:20:45.902316	confirmed	24	104622.00	2026-04-26 19:20:45.835693	\N	4
40	9	2026-03-14 18:20:45.903509	2026-03-17 18:20:45.903509	confirmed	24	92418.00	2026-04-26 19:20:45.835693	\N	3
41	5	2026-04-07 18:20:45.905219	2026-04-10 18:20:45.905219	confirmed	24	26930.00	2026-04-26 19:20:45.835693	\N	2
42	6	2026-04-01 18:20:45.906506	2026-04-05 18:20:45.906506	confirmed	25	96372.00	2026-04-26 19:20:45.835693	\N	1
43	21	2026-03-19 18:20:45.907699	2026-03-22 18:20:45.907699	confirmed	25	57860.00	2026-04-26 19:20:45.835693	\N	1
44	15	2026-02-28 18:20:45.908893	2026-03-05 18:20:45.908893	confirmed	25	54766.00	2026-04-26 19:20:45.835693	\N	2
45	18	2026-02-26 18:20:45.910075	2026-03-02 18:20:45.910075	confirmed	25	155466.00	2026-04-26 19:20:45.835693	\N	1
46	25	2026-04-02 18:20:45.911286	2026-04-07 18:20:45.911286	confirmed	25	116754.00	2026-04-26 19:20:45.835693	\N	1
\.


--
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_methods (id, name) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, method_id, amount, is_paid, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_tokens (id, user_id, token, is_revoked, expires_at) FROM stdin;
1	24	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoidGVzdEBleGFtcGxlMS5jb20iLCJyb2xlIjoiVVNFUiIsImV4cCI6MTc3NTQyMDIwNH0._ff0ybVt_GzHQXO-yMV4P6UKFkgv8vRk5RwbBISbSXQ	f	2026-04-06 02:16:44.061179+06
25	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5NzYzM30.3LyQyknCp-PqDRa6VDi-uHlxv8qJz7llWvUeBxIETy4	f	2026-04-15 02:13:53.29518+06
26	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5ODA5N30.moTB3ItPnw1Y76SuKJqEx419-DD-we0tFMNd3BEJwv0	f	2026-04-15 02:21:37.355074+06
4	24	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoidGVzdEBleGFtcGxlMS5jb20iLCJyb2xlIjoiVVNFUiIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzc1NDIxNjc3fQ.fklo0kJv_sTesBxwE48Lm3WRkLW83J95eUX8ZnGmAzA	f	2026-04-06 02:41:17.979434+06
5	24	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoidGVzdEBleGFtcGxlMS5jb20iLCJyb2xlIjoiVVNFUiIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzc1NDIxNzg5fQ.Nf5oYaSpyJ8-Cb9ivwGPeg0I7-7AK1evyHvBdCfojMk	f	2026-04-06 02:43:09.08467+06
27	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5OTQ1M30.PXBvIJw2NYx1uk95bWOIGTMjBt6xH3mpFJBICGtzCyo	f	2026-04-15 02:44:13.536795+06
28	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5OTcwOH0.xpP1G3IaAWGuzYl0To7uJgb2YJGnOjUYL66p0xZwCUY	f	2026-04-15 02:48:28.206467+06
8	24	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoidGVzdEBleGFtcGxlMS5jb20iLCJyb2xlIjoiVVNFUiIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzc1NDIyMDM1fQ.irwSKMihgHgltlcBsOubWCbWpNb5D6Uw5rLhnTXPB6I	f	2026-04-06 02:47:15.440523+06
9	24	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNCIsImVtYWlsIjoidGVzdEBleGFtcGxlMS5jb20iLCJyb2xlIjoiVVNFUiIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzc1NDIyMTQ0fQ.DWPuM5CBnStuc5dvZf9BTR-q8wgZOQSiJ-xgtK4pInM	f	2026-04-06 02:49:04.640362+06
10	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU0MjI0NTJ9.qEOJmN7FIv6lLeIjqT87TC6IBjKytdHJlY6iLjIXpG4	f	2026-04-06 02:54:12.102764+06
29	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjI4NjQzMX0.Gos5vgasQx0XjbtMb7z_TPr6O1zhZcmH_bXTbZgn5do	f	2026-04-16 02:53:51.58792+06
13	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU0MjM3MTV9.gbwBOrRMHwxNOAg139F83Sct0DLFRqarat_HbbrV-UQ	f	2026-04-06 03:15:15.139092+06
14	20	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMCIsImVtYWlsIjoiaG9wZUBob3BlLmNvbSIsInJvbGUiOiJVU0VSIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2Nzk5ODF9._0PR6XTcDiQEFbipG6vamrElK3e5XzTLR_oxXcm5WKo	f	2026-04-09 02:26:21.000109+06
15	20	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMCIsImVtYWlsIjoiaG9wZUBob3BlLmNvbSIsInJvbGUiOiJVU0VSIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2ODAxODF9.vg0jeSJovtEsxpUYqsgYtVBNtKF5FQhcnMfxp3Z3UTA	f	2026-04-09 02:29:41.82296+06
16	20	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMCIsImVtYWlsIjoiaG9wZUBob3BlLmNvbSIsInJvbGUiOiJVU0VSIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2ODA4NTJ9.Sx0qvlocvX-p_bpghKACbvtB_rX9H9nptJnkR0HVR_I	f	2026-04-09 02:40:52.15262+06
17	20	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMCIsImVtYWlsIjoiaG9wZUBob3BlLmNvbSIsInJvbGUiOiJVU0VSIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2ODEwNDR9.DgGHcllI70YlYxxXurCVf_nlYSmoUUYm8iZMZHca_O8	f	2026-04-09 02:44:04.089641+06
18	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2ODIwNzV9.0d7T0A03o4sH65tqa_CiMl5_qz8MRn7_lxmB3Cc2-Gw	f	2026-04-09 03:01:15.581728+06
19	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU2ODIyOTd9.WiJQ15E1ERUi002pgfzw5krhjkNgP7m23nacWOCSmPI	f	2026-04-09 03:04:57.468644+06
20	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU3MDk2NjN9.uZYTrsgKCGKqiUz-iVWYJta5aysiljw6fo6UKKGiKmI	f	2026-04-09 10:41:03.581659+06
21	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU4MjIyODd9.ruosjPJn8Fy0WTz-rnfdpKgjbJEdsdhRrFKLOpNGb5M	f	2026-04-10 17:58:07.671453+06
22	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzU4MjI0ODB9.tMgJqAsI91tqNEOIYTe8HsiMHj3VoKUhugj9UVrip8U	f	2026-04-10 18:01:20.721494+06
23	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5NzM3N30.xxFJCLn_FR1ZCwFNxVJv3SCmE413LN2SxYLw8Unm9cM	f	2026-04-15 02:09:37.001714+06
24	25	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNSIsImVtYWlsIjoiYmVrYWxlazRpazFAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjE5NzM4NH0.vA_tVHV3nwQZMSIsjW2xJdc7PBcE5VzjLwBy4t4Xocc	f	2026-04-15 02:09:44.80529+06
30	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4MzU0MzZ9.dhhWD2D9FhYN-Ptl2LXk-6tURbepfEy_9G1SWmdxzgo	f	2026-04-22 11:23:56.134039+06
31	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4MzU2ODF9.P0Fadjyx77k9Kd6J08PMJaZlyPH-cx5vOKjZS7JMcNY	f	2026-04-22 11:28:01.408467+06
32	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4MzU4NTl9.YiPm8Vt70FFLKJK7RC1qiUZGGNoxGgGV-EGuRTuBpIc	f	2026-04-22 11:30:59.861576+06
33	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4MzYyMDl9.FW-bbiwgbFmgvc1RnPK5e3bPD3NpjyEtcPvCO4qqfhk	f	2026-04-22 11:36:49.114055+06
34	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4NDg5Njd9.U2IaU7OAfL7wg_c8rEdqHIeDIcFm6zAgffmJ2YmCOdE	f	2026-04-22 15:09:27.091892+06
35	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4NDk4NjJ9.kIkPuUi8LZzL-71I9zEk4SIeg6k55HVTA9nUqflRiMk	f	2026-04-22 15:24:22.059012+06
36	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4NTA4MzZ9.6haecudU-69yl2H7PYEg3-XllCiXHjrC-xVUF44ocGs	f	2026-04-22 15:40:36.331105+06
37	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4NTExNjh9.bY4DwCylIH14SdPayYV5k7-KWhmdcGrUWwDLsGt8BNU	f	2026-04-22 15:46:08.418365+06
38	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzY4NTM0MjZ9.fj-OMkLiKApY6Jm2xQ9FXIKldXaEZXKw3fZd-kwJFfI	f	2026-04-22 16:23:46.294992+06
39	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzczODExNDl9.2JXkZ0LBgFncV4wqbi-WqROtL55iqsnp0v97mfeOdC4	f	2026-04-28 18:59:09.317266+06
40	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzczODE0Mjh9.QVybPC5cKjOehvBMpbCIrHAGzWbYc6CLUOk2-FP412Q	f	2026-04-28 19:03:48.323877+06
41	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzczODE2Mjd9.aup5P9qP2t3kus86UdvJOITwKL455gNEfY7VkJ-HNzU	f	2026-04-28 19:07:07.839141+06
42	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzczODE3MDZ9.luhZhOKDLAdL2F7RFK67rDwWDw1YSYTHI8bqoXZZI2s	f	2026-04-28 19:08:26.875419+06
43	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NzczODI0NzV9.InDdoOqcvHTtTGsve71DHDtdLLx7_MpsbcExlCIN-uo	f	2026-04-28 19:21:15.328526+06
44	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3Nzc1MjM0Mjh9.NM1C-HQGgqqw10njIQuYMd05vfmhOye-MvEKXFqIZCg	f	2026-04-30 10:30:28.675309+06
45	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3Nzc1MjQwNTF9.a12_ExtnH0XltInlEzcz59ImvW7t-UoR4cEfKx8WmXg	f	2026-04-30 10:40:51.888335+06
46	18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOCIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZSI6IkFETUlOIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3Nzc2OTk4NTJ9.LNPMmI-rkw1-bWvqI772ejAvyht31tKY2Y15SoJI1GI	f	2026-05-02 11:30:52.076893+06
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.review (id, user_id, booking_id, hotel_id, rating, comment, created_at) FROM stdin;
1	13	1	4	3.00	╨Э╨╛╤А╨╝╨░╨╗╤М╨╜╨╛, ╨╜╨╛ ╨▓ ╨╜╨╛╨╝╨╡╤А╨╡ ╨▒╤Л╨╗╨╛ ╤И╤Г╨╝╨╜╨╛.	2026-04-26 19:20:45.835693
2	13	2	5	4.00	╨Т╤Б╨╡ ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М, ╨╜╨╛ ╨╖╨░╨▓╤В╤А╨░╨║ ╨╝╨╛╨│ ╨▒╤Л╤В╤М ╨╗╤Г╤З╤И╨╡.	2026-04-26 19:20:45.835693
3	13	3	3	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
4	13	4	5	5.00	╨Ы╤Г╤З╤И╨╕╨╣ ╨╛╤В╨╡╨╗╤М ╨▓ ╨╝╨╛╨╡╨╣ ╨╢╨╕╨╖╨╜╨╕.	2026-04-26 19:20:45.835693
5	14	5	3	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
6	14	6	3	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
7	14	7	3	4.00	╨г╨┤╨╛╨▒╨╜╨╛╨╡ ╤А╨░╤Б╨┐╨╛╨╗╨╛╨╢╨╡╨╜╨╕╨╡.	2026-04-26 19:20:45.835693
8	15	8	5	3.00	╨Э╨╛╤А╨╝╨░╨╗╤М╨╜╨╛, ╨╜╨╛ ╨▓ ╨╜╨╛╨╝╨╡╤А╨╡ ╨▒╤Л╨╗╨╛ ╤И╤Г╨╝╨╜╨╛.	2026-04-26 19:20:45.835693
9	15	9	2	4.00	╨г╨┤╨╛╨▒╨╜╨╛╨╡ ╤А╨░╤Б╨┐╨╛╨╗╨╛╨╢╨╡╨╜╨╕╨╡.	2026-04-26 19:20:45.835693
10	15	10	3	3.00	╨Э╨╛╤А╨╝╨░╨╗╤М╨╜╨╛, ╨╜╨╛ ╨▓ ╨╜╨╛╨╝╨╡╤А╨╡ ╨▒╤Л╨╗╨╛ ╤И╤Г╨╝╨╜╨╛.	2026-04-26 19:20:45.835693
11	16	11	3	5.00	╨Ы╤Г╤З╤И╨╕╨╣ ╨╛╤В╨╡╨╗╤М ╨▓ ╨╝╨╛╨╡╨╣ ╨╢╨╕╨╖╨╜╨╕.	2026-04-26 19:20:45.835693
12	16	12	4	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
13	16	13	5	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
14	16	14	3	4.00	╨Т╤Б╨╡ ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М, ╨╜╨╛ ╨╖╨░╨▓╤В╤А╨░╨║ ╨╝╨╛╨│ ╨▒╤Л╤В╤М ╨╗╤Г╤З╤И╨╡.	2026-04-26 19:20:45.835693
15	17	15	3	3.00	╨Ю╨▒╤Л╤З╨╜╤Л╨╣ ╨╛╤В╨╡╨╗╤М. ╨Э╨╕╤З╨╡╨│╨╛ ╨╛╤Б╨╛╨▒╨╡╨╜╨╜╨╛╨│╨╛.	2026-04-26 19:20:45.835693
16	17	16	2	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
17	17	17	5	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
18	18	18	2	5.00	╨Я╤А╨╡╨▓╨╛╤Б╤Е╨╛╨┤╨╜╨╛! ╨Ю╤З╨╡╨╜╤М ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М.	2026-04-26 19:20:45.835693
19	18	19	2	5.00	╨Я╤А╨╡╨▓╨╛╤Б╤Е╨╛╨┤╨╜╨╛! ╨Ю╤З╨╡╨╜╤М ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М.	2026-04-26 19:20:45.835693
20	18	20	4	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
21	18	21	3	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
22	19	22	4	4.00	╨Т╤Б╨╡ ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М, ╨╜╨╛ ╨╖╨░╨▓╤В╤А╨░╨║ ╨╝╨╛╨│ ╨▒╤Л╤В╤М ╨╗╤Г╤З╤И╨╡.	2026-04-26 19:20:45.835693
23	19	23	2	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
24	19	24	5	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
25	19	25	4	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
26	19	26	4	3.00	╨Ю╨▒╤Л╤З╨╜╤Л╨╣ ╨╛╤В╨╡╨╗╤М. ╨Э╨╕╤З╨╡╨│╨╛ ╨╛╤Б╨╛╨▒╨╡╨╜╨╜╨╛╨│╨╛.	2026-04-26 19:20:45.835693
27	20	27	4	5.00	╨Я╤А╨╡╨▓╨╛╤Б╤Е╨╛╨┤╨╜╨╛! ╨Ю╤З╨╡╨╜╤М ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М.	2026-04-26 19:20:45.835693
28	20	28	1	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
29	20	29	1	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
30	20	30	1	5.00	╨Ы╤Г╤З╤И╨╕╨╣ ╨╛╤В╨╡╨╗╤М ╨▓ ╨╝╨╛╨╡╨╣ ╨╢╨╕╨╖╨╜╨╕.	2026-04-26 19:20:45.835693
31	20	31	2	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
32	22	32	2	4.00	╨е╨╛╤А╨╛╤И╨╡╨╡ ╨╝╨╡╤Б╤В╨╛, ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╤Г╤О.	2026-04-26 19:20:45.835693
33	22	33	2	5.00	╨Ы╤Г╤З╤И╨╕╨╣ ╨╛╤В╨╡╨╗╤М ╨▓ ╨╝╨╛╨╡╨╣ ╨╢╨╕╨╖╨╜╨╕.	2026-04-26 19:20:45.835693
34	22	34	3	3.00	╨Ю╨▒╤Л╤З╨╜╤Л╨╣ ╨╛╤В╨╡╨╗╤М. ╨Э╨╕╤З╨╡╨│╨╛ ╨╛╤Б╨╛╨▒╨╡╨╜╨╜╨╛╨│╨╛.	2026-04-26 19:20:45.835693
35	22	35	4	5.00	╨Я╤А╨╡╨▓╨╛╤Б╤Е╨╛╨┤╨╜╨╛! ╨Ю╤З╨╡╨╜╤М ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М.	2026-04-26 19:20:45.835693
36	23	36	3	5.00	╨Я╤А╨╡╨▓╨╛╤Б╤Е╨╛╨┤╨╜╨╛! ╨Ю╤З╨╡╨╜╤М ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М.	2026-04-26 19:20:45.835693
37	23	37	1	4.00	╨Т╤Б╨╡ ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М, ╨╜╨╛ ╨╖╨░╨▓╤В╤А╨░╨║ ╨╝╨╛╨│ ╨▒╤Л╤В╤М ╨╗╤Г╤З╤И╨╡.	2026-04-26 19:20:45.835693
38	23	38	4	3.00	╨Ю╨▒╤Л╤З╨╜╤Л╨╣ ╨╛╤В╨╡╨╗╤М. ╨Э╨╕╤З╨╡╨│╨╛ ╨╛╤Б╨╛╨▒╨╡╨╜╨╜╨╛╨│╨╛.	2026-04-26 19:20:45.835693
39	24	39	4	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
40	24	40	2	3.00	╨Ю╨▒╤Л╤З╨╜╤Л╨╣ ╨╛╤В╨╡╨╗╤М. ╨Э╨╕╤З╨╡╨│╨╛ ╨╛╤Б╨╛╨▒╨╡╨╜╨╜╨╛╨│╨╛.	2026-04-26 19:20:45.835693
41	24	41	1	4.00	╨Т╤Б╨╡ ╨┐╨╛╨╜╤А╨░╨▓╨╕╨╗╨╛╤Б╤М, ╨╜╨╛ ╨╖╨░╨▓╤В╤А╨░╨║ ╨╝╨╛╨│ ╨▒╤Л╤В╤М ╨╗╤Г╤З╤И╨╡.	2026-04-26 19:20:45.835693
42	25	42	2	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
43	25	43	5	4.00	╨г╨┤╨╛╨▒╨╜╨╛╨╡ ╤А╨░╤Б╨┐╨╛╨╗╨╛╨╢╨╡╨╜╨╕╨╡.	2026-04-26 19:20:45.835693
44	25	44	3	5.00	╨з╨╕╤Б╤В╨╛, ╤Г╤О╤В╨╜╨╛, ╤Б╨╡╤А╨▓╨╕╤Б 10/10.	2026-04-26 19:20:45.835693
45	25	45	4	3.00	╨ж╨╡╨╜╨░ ╤Б╨╛╨╛╤В╨▓╨╡╤В╤Б╤В╨▓╤Г╨╡╤В ╨║╨░╤З╨╡╤Б╤В╨▓╤Г.	2026-04-26 19:20:45.835693
46	25	46	5	4.00	╨г╨┤╨╛╨▒╨╜╨╛╨╡ ╤А╨░╤Б╨┐╨╛╨╗╨╛╨╢╨╡╨╜╨╕╨╡.	2026-04-26 19:20:45.835693
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transactions (id, booking_id, type, created_at, payment_id) FROM stdin;
\.


--
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id_seq', 46, true);


--
-- Name: cancellation_policy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cancellation_policy_id_seq', 1, false);


--
-- Name: hotels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hotels_id_seq', 5, true);


--
-- Name: payment_methods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payment_methods_id_seq', 1, false);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 46, true);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.review_id_seq', 46, true);


--
-- Name: room_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.room_types_id_seq', 10, true);


--
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 25, true);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transactions_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 25, true);


--
-- PostgreSQL database dump complete
--

