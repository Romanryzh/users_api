--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Ubuntu 16.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-1.pgdg20.04+1)

-- Started on 2024-09-03 10:38:34 PDT

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3301 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 24580)
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    last_name text NOT NULL,
    phone_number text NOT NULL,
    age integer NOT NULL,
    first_name text NOT NULL
);


ALTER TABLE public.users OWNER TO admin;

--
-- TOC entry 3295 (class 0 OID 24580)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, last_name, phone_number, age, first_name) FROM stdin;
\.


-- Completed on 2024-09-03 10:38:34 PDT

--
-- PostgreSQL database dump complete
--

