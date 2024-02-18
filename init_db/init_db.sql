--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: funnel; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.funnel (
                               id integer NOT NULL,
                               user_id integer,
                               send_time timestamp without time zone NOT NULL,
                               text text NOT NULL,
                               status integer,
                               status_updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
                               level integer NOT NULL
);


ALTER TABLE public.funnel OWNER TO app;

--
-- Name: funnel_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

ALTER TABLE public.funnel ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.funnel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    );


--
-- Name: funnel_status; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.funnel_status (
                                      id integer NOT NULL,
                                      status character varying(16)
);


ALTER TABLE public.funnel_status OWNER TO app;

--
-- Name: funnel_status_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

ALTER TABLE public.funnel_status ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.funnel_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    );


--
-- Name: status; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.status (
                               id integer NOT NULL,
                               status character varying(16) NOT NULL
);


ALTER TABLE public.status OWNER TO app;

--
-- Name: status_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

ALTER TABLE public.status ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    );


--
-- Name: user; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public."user" (
                               id integer NOT NULL,
                               user_id bigint NOT NULL,
                               created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
                               status_updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
                               status integer DEFAULT 1 NOT NULL,
                               last_message_id bigint,
                               username character varying(255)
);


ALTER TABLE public."user" OWNER TO app;

--
-- Name: COLUMN "user".user_id; Type: COMMENT; Schema: public; Owner: app
--

COMMENT ON COLUMN public."user".user_id IS 'Telegram user id';


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

ALTER TABLE public."user" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    );


--
-- Name: funnel funnel_pk; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.funnel
    ADD CONSTRAINT funnel_pk PRIMARY KEY (id);


--
-- Name: funnel_status funnel_status_pk; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.funnel_status
    ADD CONSTRAINT funnel_status_pk PRIMARY KEY (id);


--
-- Name: status status_pk; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pk PRIMARY KEY (id);


--
-- Name: user user_pk; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- Name: user__tg_uindex; Type: INDEX; Schema: public; Owner: app
--

CREATE UNIQUE INDEX user__tg_uindex ON public."user" USING btree (user_id);


--
-- Name: funnel funnel_funnel_status_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.funnel
    ADD CONSTRAINT funnel_funnel_status_id_fk FOREIGN KEY (status) REFERENCES public.funnel_status(id);


--
-- Name: funnel funnel_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.funnel
    ADD CONSTRAINT funnel_user_id_fk FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user user___status; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user___status FOREIGN KEY (status) REFERENCES public.status(id);


--
-- PostgreSQL database dump complete
--