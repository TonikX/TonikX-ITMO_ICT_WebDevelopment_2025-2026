--
-- PostgreSQL database dump
--

\restrict ghhGAgPqnd51jrMZxbvnAb5BeeHMCUTmCP5i2FxPQJjJXIxbHBT0nbpO8a7bKeh

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2025-11-26 01:49:27

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 5187 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 239 (class 1255 OID 24975)
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_updated_at() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 24727)
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    author_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.author OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24726)
-- Name: author_author_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.author_author_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.author_author_id_seq OWNER TO postgres;

--
-- TOC entry 5188 (class 0 OID 0)
-- Dependencies: 219
-- Name: author_author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.author_author_id_seq OWNED BY public.author.author_id;


--
-- TOC entry 226 (class 1259 OID 24770)
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    book_id integer NOT NULL,
    title character varying(200) NOT NULL,
    publisher_id integer,
    publish_year integer,
    section_id integer,
    cipher character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.book OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24794)
-- Name: book_author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_author (
    book_id integer NOT NULL,
    author_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.book_author OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24769)
-- Name: book_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_book_id_seq OWNER TO postgres;

--
-- TOC entry 5189 (class 0 OID 0)
-- Dependencies: 225
-- Name: book_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_book_id_seq OWNED BY public.book.book_id;


--
-- TOC entry 235 (class 1259 OID 24887)
-- Name: book_copy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_copy (
    copy_id integer NOT NULL,
    book_id integer NOT NULL,
    hall_id integer NOT NULL,
    inventory_number character varying(50) NOT NULL,
    registration_date date DEFAULT CURRENT_DATE NOT NULL,
    writeoff_date date,
    is_written_off boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT book_copy_check CHECK ((((is_written_off = false) AND (writeoff_date IS NULL)) OR ((is_written_off = true) AND (writeoff_date IS NOT NULL))))
);


ALTER TABLE public.book_copy OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 24886)
-- Name: book_copy_copy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_copy_copy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_copy_copy_id_seq OWNER TO postgres;

--
-- TOC entry 5190 (class 0 OID 0)
-- Dependencies: 234
-- Name: book_copy_copy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_copy_copy_id_seq OWNED BY public.book_copy.copy_id;


--
-- TOC entry 238 (class 1259 OID 24944)
-- Name: book_issue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_issue (
    issue_id integer NOT NULL,
    reader_id integer NOT NULL,
    copy_id integer NOT NULL,
    issue_date date DEFAULT CURRENT_DATE NOT NULL,
    return_date date,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    hall_id integer NOT NULL,
    CONSTRAINT book_issue_check CHECK (((return_date IS NULL) OR (return_date >= issue_date)))
);


ALTER TABLE public.book_issue OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 24943)
-- Name: book_issue_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_issue_issue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_issue_issue_id_seq OWNER TO postgres;

--
-- TOC entry 5191 (class 0 OID 0)
-- Dependencies: 237
-- Name: book_issue_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_issue_issue_id_seq OWNED BY public.book_issue.issue_id;


--
-- TOC entry 224 (class 1259 OID 24755)
-- Name: book_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_section (
    section_id integer NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.book_section OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24754)
-- Name: book_section_section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_section_section_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_section_section_id_seq OWNER TO postgres;

--
-- TOC entry 5192 (class 0 OID 0)
-- Dependencies: 223
-- Name: book_section_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_section_section_id_seq OWNED BY public.book_section.section_id;


--
-- TOC entry 229 (class 1259 OID 24816)
-- Name: hall; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hall (
    hall_id integer NOT NULL,
    hall_number integer NOT NULL,
    name character varying(100) NOT NULL,
    capacity integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.hall OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 24920)
-- Name: hall_book_stock; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hall_book_stock (
    hall_id integer NOT NULL,
    book_id integer NOT NULL,
    copies_total integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.hall_book_stock OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 24815)
-- Name: hall_hall_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hall_hall_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hall_hall_id_seq OWNER TO postgres;

--
-- TOC entry 5193 (class 0 OID 0)
-- Dependencies: 228
-- Name: hall_hall_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hall_hall_id_seq OWNED BY public.hall.hall_id;


--
-- TOC entry 222 (class 1259 OID 24740)
-- Name: publisher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publisher (
    publisher_id integer NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.publisher OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24739)
-- Name: publisher_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.publisher_publisher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.publisher_publisher_id_seq OWNER TO postgres;

--
-- TOC entry 5194 (class 0 OID 0)
-- Dependencies: 221
-- Name: publisher_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.publisher_publisher_id_seq OWNED BY public.publisher.publisher_id;


--
-- TOC entry 231 (class 1259 OID 24833)
-- Name: reader; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reader (
    reader_id integer NOT NULL,
    card_number character varying(20) NOT NULL,
    full_name character varying(100) NOT NULL,
    passport_number character varying(11) NOT NULL,
    birth_date date NOT NULL,
    address character varying(200),
    phone character varying(20),
    education_level character varying(20),
    has_academic_degree boolean DEFAULT false NOT NULL,
    hall_id integer,
    registration_date date DEFAULT CURRENT_DATE NOT NULL,
    last_reregistration_date date,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reader OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 24832)
-- Name: reader_reader_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reader_reader_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reader_reader_id_seq OWNER TO postgres;

--
-- TOC entry 5195 (class 0 OID 0)
-- Dependencies: 230
-- Name: reader_reader_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reader_reader_id_seq OWNED BY public.reader.reader_id;


--
-- TOC entry 233 (class 1259 OID 24866)
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    staff_id integer NOT NULL,
    login character varying(50) NOT NULL,
    email character varying(150) NOT NULL,
    password_hash character varying(512) NOT NULL,
    refresh_token character varying(256),
    refresh_token_expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.staff OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 24865)
-- Name: staff_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_staff_id_seq OWNER TO postgres;

--
-- TOC entry 5196 (class 0 OID 0)
-- Dependencies: 232
-- Name: staff_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_staff_id_seq OWNED BY public.staff.staff_id;


--
-- TOC entry 4905 (class 2604 OID 24730)
-- Name: author author_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author ALTER COLUMN author_id SET DEFAULT nextval('public.author_author_id_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 24773)
-- Name: book book_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN book_id SET DEFAULT nextval('public.book_book_id_seq'::regclass);


--
-- TOC entry 4931 (class 2604 OID 24890)
-- Name: book_copy copy_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_copy ALTER COLUMN copy_id SET DEFAULT nextval('public.book_copy_copy_id_seq'::regclass);


--
-- TOC entry 4938 (class 2604 OID 24947)
-- Name: book_issue issue_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue ALTER COLUMN issue_id SET DEFAULT nextval('public.book_issue_issue_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 24758)
-- Name: book_section section_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_section ALTER COLUMN section_id SET DEFAULT nextval('public.book_section_section_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 24819)
-- Name: hall hall_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall ALTER COLUMN hall_id SET DEFAULT nextval('public.hall_hall_id_seq'::regclass);


--
-- TOC entry 4908 (class 2604 OID 24743)
-- Name: publisher publisher_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publisher ALTER COLUMN publisher_id SET DEFAULT nextval('public.publisher_publisher_id_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 24836)
-- Name: reader reader_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reader ALTER COLUMN reader_id SET DEFAULT nextval('public.reader_reader_id_seq'::regclass);


--
-- TOC entry 4928 (class 2604 OID 24869)
-- Name: staff staff_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff ALTER COLUMN staff_id SET DEFAULT nextval('public.staff_staff_id_seq'::regclass);


--
-- TOC entry 5163 (class 0 OID 24727)
-- Dependencies: 220
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.author (author_id, full_name, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5169 (class 0 OID 24770)
-- Dependencies: 226
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book (book_id, title, publisher_id, publish_year, section_id, cipher, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5170 (class 0 OID 24794)
-- Dependencies: 227
-- Data for Name: book_author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_author (book_id, author_id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5178 (class 0 OID 24887)
-- Dependencies: 235
-- Data for Name: book_copy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_copy (copy_id, book_id, hall_id, inventory_number, registration_date, writeoff_date, is_written_off, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5181 (class 0 OID 24944)
-- Dependencies: 238
-- Data for Name: book_issue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_issue (issue_id, reader_id, copy_id, issue_date, return_date, created_at, updated_at, hall_id) FROM stdin;
\.


--
-- TOC entry 5167 (class 0 OID 24755)
-- Dependencies: 224
-- Data for Name: book_section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_section (section_id, name, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5172 (class 0 OID 24816)
-- Dependencies: 229
-- Data for Name: hall; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hall (hall_id, hall_number, name, capacity, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5179 (class 0 OID 24920)
-- Dependencies: 236
-- Data for Name: hall_book_stock; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hall_book_stock (hall_id, book_id, copies_total, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5165 (class 0 OID 24740)
-- Dependencies: 222
-- Data for Name: publisher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publisher (publisher_id, name, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5174 (class 0 OID 24833)
-- Dependencies: 231
-- Data for Name: reader; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reader (reader_id, card_number, full_name, passport_number, birth_date, address, phone, education_level, has_academic_degree, hall_id, registration_date, last_reregistration_date, is_active, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5176 (class 0 OID 24866)
-- Dependencies: 233
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff (staff_id, login, email, password_hash, refresh_token, refresh_token_expires_at, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5197 (class 0 OID 0)
-- Dependencies: 219
-- Name: author_author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.author_author_id_seq', 1, false);


--
-- TOC entry 5198 (class 0 OID 0)
-- Dependencies: 225
-- Name: book_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_book_id_seq', 1, false);


--
-- TOC entry 5199 (class 0 OID 0)
-- Dependencies: 234
-- Name: book_copy_copy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_copy_copy_id_seq', 1, false);


--
-- TOC entry 5200 (class 0 OID 0)
-- Dependencies: 237
-- Name: book_issue_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_issue_issue_id_seq', 1, false);


--
-- TOC entry 5201 (class 0 OID 0)
-- Dependencies: 223
-- Name: book_section_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_section_section_id_seq', 1, false);


--
-- TOC entry 5202 (class 0 OID 0)
-- Dependencies: 228
-- Name: hall_hall_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hall_hall_id_seq', 1, false);


--
-- TOC entry 5203 (class 0 OID 0)
-- Dependencies: 221
-- Name: publisher_publisher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.publisher_publisher_id_seq', 1, false);


--
-- TOC entry 5204 (class 0 OID 0)
-- Dependencies: 230
-- Name: reader_reader_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reader_reader_id_seq', 1, false);


--
-- TOC entry 5205 (class 0 OID 0)
-- Dependencies: 232
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 1, false);


--
-- TOC entry 4945 (class 2606 OID 24738)
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (author_id);


--
-- TOC entry 4958 (class 2606 OID 24804)
-- Name: book_author book_author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_pkey PRIMARY KEY (book_id, author_id);


--
-- TOC entry 4978 (class 2606 OID 24907)
-- Name: book_copy book_copy_inventory_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_copy
    ADD CONSTRAINT book_copy_inventory_number_key UNIQUE (inventory_number);


--
-- TOC entry 4980 (class 2606 OID 24905)
-- Name: book_copy book_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_copy
    ADD CONSTRAINT book_copy_pkey PRIMARY KEY (copy_id);


--
-- TOC entry 4987 (class 2606 OID 24959)
-- Name: book_issue book_issue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue
    ADD CONSTRAINT book_issue_pkey PRIMARY KEY (issue_id);


--
-- TOC entry 4955 (class 2606 OID 24782)
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (book_id);


--
-- TOC entry 4951 (class 2606 OID 24768)
-- Name: book_section book_section_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_section
    ADD CONSTRAINT book_section_name_key UNIQUE (name);


--
-- TOC entry 4953 (class 2606 OID 24766)
-- Name: book_section book_section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_section
    ADD CONSTRAINT book_section_pkey PRIMARY KEY (section_id);


--
-- TOC entry 4984 (class 2606 OID 24931)
-- Name: hall_book_stock hall_book_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall_book_stock
    ADD CONSTRAINT hall_book_stock_pkey PRIMARY KEY (hall_id, book_id);


--
-- TOC entry 4960 (class 2606 OID 24831)
-- Name: hall hall_hall_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall
    ADD CONSTRAINT hall_hall_number_key UNIQUE (hall_number);


--
-- TOC entry 4962 (class 2606 OID 24829)
-- Name: hall hall_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall
    ADD CONSTRAINT hall_pkey PRIMARY KEY (hall_id);


--
-- TOC entry 4947 (class 2606 OID 24753)
-- Name: publisher publisher_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publisher
    ADD CONSTRAINT publisher_name_key UNIQUE (name);


--
-- TOC entry 4949 (class 2606 OID 24751)
-- Name: publisher publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publisher
    ADD CONSTRAINT publisher_pkey PRIMARY KEY (publisher_id);


--
-- TOC entry 4966 (class 2606 OID 24855)
-- Name: reader reader_card_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reader
    ADD CONSTRAINT reader_card_number_key UNIQUE (card_number);


--
-- TOC entry 4968 (class 2606 OID 24857)
-- Name: reader reader_passport_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reader
    ADD CONSTRAINT reader_passport_number_key UNIQUE (passport_number);


--
-- TOC entry 4970 (class 2606 OID 24853)
-- Name: reader reader_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reader
    ADD CONSTRAINT reader_pkey PRIMARY KEY (reader_id);


--
-- TOC entry 4972 (class 2606 OID 24885)
-- Name: staff staff_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_email_key UNIQUE (email);


--
-- TOC entry 4974 (class 2606 OID 24883)
-- Name: staff staff_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_login_key UNIQUE (login);


--
-- TOC entry 4976 (class 2606 OID 24881)
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


--
-- TOC entry 4956 (class 1259 OID 24793)
-- Name: idx_book_cipher; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_book_cipher ON public.book USING btree (cipher);


--
-- TOC entry 4981 (class 1259 OID 24918)
-- Name: idx_copy_book; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_copy_book ON public.book_copy USING btree (book_id);


--
-- TOC entry 4982 (class 1259 OID 24919)
-- Name: idx_copy_hall; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_copy_hall ON public.book_copy USING btree (hall_id);


--
-- TOC entry 4988 (class 1259 OID 24971)
-- Name: idx_issue_copy; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_issue_copy ON public.book_issue USING btree (copy_id);


--
-- TOC entry 4989 (class 1259 OID 24972)
-- Name: idx_issue_dates; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_issue_dates ON public.book_issue USING btree (issue_date, return_date);


--
-- TOC entry 4990 (class 1259 OID 24970)
-- Name: idx_issue_reader; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_issue_reader ON public.book_issue USING btree (reader_id);


--
-- TOC entry 4963 (class 1259 OID 24863)
-- Name: idx_reader_birth; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reader_birth ON public.reader USING btree (birth_date);


--
-- TOC entry 4964 (class 1259 OID 24864)
-- Name: idx_reader_hall; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reader_hall ON public.reader USING btree (hall_id);


--
-- TOC entry 4985 (class 1259 OID 24942)
-- Name: idx_stock_book; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_stock_book ON public.hall_book_stock USING btree (book_id);


--
-- TOC entry 4991 (class 1259 OID 24973)
-- Name: uq_issue_active_per_copy; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_issue_active_per_copy ON public.book_issue USING btree (copy_id) WHERE (return_date IS NULL);


--
-- TOC entry 5004 (class 2620 OID 24976)
-- Name: author trg_set_updated_at_author; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_author BEFORE UPDATE ON public.author FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5007 (class 2620 OID 24979)
-- Name: book trg_set_updated_at_book; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_book BEFORE UPDATE ON public.book FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5008 (class 2620 OID 24980)
-- Name: book_author trg_set_updated_at_book_author; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_book_author BEFORE UPDATE ON public.book_author FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5012 (class 2620 OID 24984)
-- Name: book_copy trg_set_updated_at_book_copy; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_book_copy BEFORE UPDATE ON public.book_copy FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5014 (class 2620 OID 24986)
-- Name: book_issue trg_set_updated_at_book_issue; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_book_issue BEFORE UPDATE ON public.book_issue FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5006 (class 2620 OID 24978)
-- Name: book_section trg_set_updated_at_book_section; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_book_section BEFORE UPDATE ON public.book_section FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5009 (class 2620 OID 24981)
-- Name: hall trg_set_updated_at_hall; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_hall BEFORE UPDATE ON public.hall FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5013 (class 2620 OID 24985)
-- Name: hall_book_stock trg_set_updated_at_hall_book_stock; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_hall_book_stock BEFORE UPDATE ON public.hall_book_stock FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5005 (class 2620 OID 24977)
-- Name: publisher trg_set_updated_at_publisher; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_publisher BEFORE UPDATE ON public.publisher FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5010 (class 2620 OID 24982)
-- Name: reader trg_set_updated_at_reader; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_reader BEFORE UPDATE ON public.reader FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 5011 (class 2620 OID 24983)
-- Name: staff trg_set_updated_at_staff; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_set_updated_at_staff BEFORE UPDATE ON public.staff FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- TOC entry 4994 (class 2606 OID 24810)
-- Name: book_author book_author_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.author(author_id) ON DELETE CASCADE;


--
-- TOC entry 4995 (class 2606 OID 24805)
-- Name: book_author book_author_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(book_id) ON DELETE CASCADE;


--
-- TOC entry 4997 (class 2606 OID 24908)
-- Name: book_copy book_copy_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_copy
    ADD CONSTRAINT book_copy_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(book_id) ON DELETE CASCADE;


--
-- TOC entry 4998 (class 2606 OID 24913)
-- Name: book_copy book_copy_hall_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_copy
    ADD CONSTRAINT book_copy_hall_id_fkey FOREIGN KEY (hall_id) REFERENCES public.hall(hall_id);


--
-- TOC entry 5001 (class 2606 OID 24965)
-- Name: book_issue book_issue_copy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue
    ADD CONSTRAINT book_issue_copy_id_fkey FOREIGN KEY (copy_id) REFERENCES public.book_copy(copy_id);


--
-- TOC entry 5002 (class 2606 OID 24988)
-- Name: book_issue book_issue_hall_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue
    ADD CONSTRAINT book_issue_hall_id_fkey FOREIGN KEY (hall_id) REFERENCES public.hall(hall_id);


--
-- TOC entry 5003 (class 2606 OID 24960)
-- Name: book_issue book_issue_reader_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue
    ADD CONSTRAINT book_issue_reader_id_fkey FOREIGN KEY (reader_id) REFERENCES public.reader(reader_id);


--
-- TOC entry 4992 (class 2606 OID 24783)
-- Name: book book_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.publisher(publisher_id);


--
-- TOC entry 4993 (class 2606 OID 24788)
-- Name: book book_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.book_section(section_id);


--
-- TOC entry 4999 (class 2606 OID 24937)
-- Name: hall_book_stock hall_book_stock_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall_book_stock
    ADD CONSTRAINT hall_book_stock_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(book_id) ON DELETE CASCADE;


--
-- TOC entry 5000 (class 2606 OID 24932)
-- Name: hall_book_stock hall_book_stock_hall_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall_book_stock
    ADD CONSTRAINT hall_book_stock_hall_id_fkey FOREIGN KEY (hall_id) REFERENCES public.hall(hall_id) ON DELETE CASCADE;


--
-- TOC entry 4996 (class 2606 OID 24858)
-- Name: reader reader_hall_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reader
    ADD CONSTRAINT reader_hall_id_fkey FOREIGN KEY (hall_id) REFERENCES public.hall(hall_id);


-- Completed on 2025-11-26 01:49:27

--
-- PostgreSQL database dump complete
--

\unrestrict ghhGAgPqnd51jrMZxbvnAb5BeeHMCUTmCP5i2FxPQJjJXIxbHBT0nbpO8a7bKeh

