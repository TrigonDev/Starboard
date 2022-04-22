CREATE TABLE guilds ();
CREATE TABLE users ();
CREATE TABLE members ();
CREATE TABLE starboards ();
CREATE TABLE overrides ();
CREATE TABLE permroles ();
CREATE TABLE permrole_starboards ();
CREATE TABLE aschannels ();
CREATE TABLE xproles ();
CREATE TABLE posroles ();
CREATE TABLE posrole_members ();
CREATE TABLE messages ();
CREATE TABLE sb_messages ();
CREATE TABLE stars ();
CREATE TABLE _migrations ();
ALTER TABLE guilds ADD COLUMN id NUMERIC;
ALTER TABLE guilds ADD COLUMN premium_end TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN id NUMERIC;
ALTER TABLE users ADD COLUMN is_bot BOOLEAN;
ALTER TABLE users ADD COLUMN credits INTEGER;
ALTER TABLE users ADD COLUMN donated_cents BIGINT;
ALTER TABLE users ADD COLUMN last_patreon_total_cents BIGINT;
ALTER TABLE users ADD COLUMN patreon_status SMALLINT;
ALTER TABLE members ADD COLUMN user_id NUMERIC;
ALTER TABLE members ADD COLUMN guild_id NUMERIC;
ALTER TABLE members ADD COLUMN xp INTEGER;
ALTER TABLE members ADD COLUMN autoredeem_enabled BOOLEAN;
ALTER TABLE starboards ADD COLUMN id NUMERIC;
ALTER TABLE starboards ADD COLUMN guild_id NUMERIC;
ALTER TABLE starboards ADD COLUMN webhook_id NUMERIC;
ALTER TABLE starboards ADD COLUMN color INTEGER;
ALTER TABLE starboards ADD COLUMN display_emoji TEXT;
ALTER TABLE starboards ADD COLUMN ping_author BOOLEAN;
ALTER TABLE starboards ADD COLUMN use_server_profile BOOLEAN;
ALTER TABLE starboards ADD COLUMN extra_embeds BOOLEAN;
ALTER TABLE starboards ADD COLUMN use_webhook BOOLEAN;
ALTER TABLE starboards ADD COLUMN webhook_name TEXT;
ALTER TABLE starboards ADD COLUMN webhook_avatar TEXT;
ALTER TABLE starboards ADD COLUMN required SMALLINT;
ALTER TABLE starboards ADD COLUMN required_remove SMALLINT;
ALTER TABLE starboards ADD COLUMN star_emojis TEXT[];
ALTER TABLE starboards ADD COLUMN self_star BOOLEAN;
ALTER TABLE starboards ADD COLUMN allow_bots BOOLEAN;
ALTER TABLE starboards ADD COLUMN require_image BOOLEAN;
ALTER TABLE starboards ADD COLUMN enabled BOOLEAN;
ALTER TABLE starboards ADD COLUMN autoreact BOOLEAN;
ALTER TABLE starboards ADD COLUMN remove_invalid BOOLEAN;
ALTER TABLE starboards ADD COLUMN link_deletes BOOLEAN;
ALTER TABLE starboards ADD COLUMN link_edits BOOLEAN;
ALTER TABLE starboards ADD COLUMN disable_xp BOOLEAN;
ALTER TABLE starboards ADD COLUMN private BOOLEAN;
ALTER TABLE starboards ADD COLUMN cooldown_enabled BOOLEAN;
ALTER TABLE starboards ADD COLUMN cooldown_count SMALLINT;
ALTER TABLE starboards ADD COLUMN cooldown_period SMALLINT;
ALTER TABLE overrides ADD COLUMN id SERIAL;
ALTER TABLE overrides ADD COLUMN guild_id NUMERIC;
ALTER TABLE overrides ADD COLUMN name TEXT;
ALTER TABLE overrides ADD COLUMN starboard_id NUMERIC;
ALTER TABLE overrides ADD COLUMN channel_ids NUMERIC[];
ALTER TABLE overrides ADD COLUMN _overrides JSON;
ALTER TABLE permroles ADD COLUMN id NUMERIC;
ALTER TABLE permroles ADD COLUMN guild_id NUMERIC;
ALTER TABLE permroles ADD COLUMN xproles BOOLEAN;
ALTER TABLE permroles ADD COLUMN give_stars BOOLEAN;
ALTER TABLE permroles ADD COLUMN recv_stars BOOLEAN;
ALTER TABLE permrole_starboards ADD COLUMN permrole_id NUMERIC;
ALTER TABLE permrole_starboards ADD COLUMN starboard_id NUMERIC;
ALTER TABLE permrole_starboards ADD COLUMN give_stars BOOLEAN;
ALTER TABLE permrole_starboards ADD COLUMN recv_stars BOOLEAN;
ALTER TABLE aschannels ADD COLUMN id NUMERIC;
ALTER TABLE aschannels ADD COLUMN guild_id NUMERIC;
ALTER TABLE aschannels ADD COLUMN emojis TEXT[];
ALTER TABLE aschannels ADD COLUMN min_chars SMALLINT;
ALTER TABLE aschannels ADD COLUMN max_chars SMALLINT;
ALTER TABLE aschannels ADD COLUMN require_image BOOLEAN;
ALTER TABLE aschannels ADD COLUMN delete_invalid BOOLEAN;
ALTER TABLE xproles ADD COLUMN id NUMERIC;
ALTER TABLE xproles ADD COLUMN guild_id NUMERIC;
ALTER TABLE xproles ADD COLUMN required SMALLINT;
ALTER TABLE posroles ADD COLUMN id NUMERIC;
ALTER TABLE posroles ADD COLUMN guild_id NUMERIC;
ALTER TABLE posroles ADD COLUMN max_members INTEGER;
ALTER TABLE posrole_members ADD COLUMN role_id NUMERIC;
ALTER TABLE posrole_members ADD COLUMN user_id NUMERIC;
ALTER TABLE messages ADD COLUMN id NUMERIC;
ALTER TABLE messages ADD COLUMN guild_id NUMERIC;
ALTER TABLE messages ADD COLUMN channel_id NUMERIC;
ALTER TABLE messages ADD COLUMN author_id NUMERIC;
ALTER TABLE messages ADD COLUMN is_nsfw BOOLEAN;
ALTER TABLE messages ADD COLUMN forced_to NUMERIC[];
ALTER TABLE messages ADD COLUMN trashed BOOLEAN;
ALTER TABLE messages ADD COLUMN trash_reason VARCHAR(32);
ALTER TABLE messages ADD COLUMN frozen BOOLEAN;
ALTER TABLE sb_messages ADD COLUMN message_id NUMERIC;
ALTER TABLE sb_messages ADD COLUMN starboard_id NUMERIC;
ALTER TABLE sb_messages ADD COLUMN sb_message_id NUMERIC;
ALTER TABLE sb_messages ADD COLUMN last_known_star_count SMALLINT;
ALTER TABLE stars ADD COLUMN message_id NUMERIC;
ALTER TABLE stars ADD COLUMN starboard_id NUMERIC;
ALTER TABLE stars ADD COLUMN user_id NUMERIC;
ALTER TABLE _migrations ADD COLUMN id_ INTEGER;
ALTER TABLE guilds ALTER COLUMN id SET NOT NULL;
ALTER TABLE users ALTER COLUMN id SET NOT NULL;
ALTER TABLE users ALTER COLUMN is_bot SET NOT NULL;
ALTER TABLE users ALTER COLUMN credits SET NOT NULL;
ALTER TABLE users ALTER COLUMN donated_cents SET NOT NULL;
ALTER TABLE users ALTER COLUMN last_patreon_total_cents SET NOT NULL;
ALTER TABLE users ALTER COLUMN patreon_status SET NOT NULL;
ALTER TABLE members ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE members ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE members ALTER COLUMN xp SET NOT NULL;
ALTER TABLE members ALTER COLUMN autoredeem_enabled SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN id SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN color SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN ping_author SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN use_server_profile SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN extra_embeds SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN use_webhook SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN webhook_name SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN required SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN required_remove SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN star_emojis SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN self_star SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN allow_bots SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN require_image SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN enabled SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN autoreact SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN remove_invalid SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN link_deletes SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN link_edits SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN disable_xp SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN private SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN cooldown_enabled SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN cooldown_count SET NOT NULL;
ALTER TABLE starboards ALTER COLUMN cooldown_period SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN id SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN name SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN starboard_id SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN channel_ids SET NOT NULL;
ALTER TABLE overrides ALTER COLUMN _overrides SET NOT NULL;
ALTER TABLE permroles ALTER COLUMN id SET NOT NULL;
ALTER TABLE permroles ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE permrole_starboards ALTER COLUMN permrole_id SET NOT NULL;
ALTER TABLE permrole_starboards ALTER COLUMN starboard_id SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN id SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN emojis SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN min_chars SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN require_image SET NOT NULL;
ALTER TABLE aschannels ALTER COLUMN delete_invalid SET NOT NULL;
ALTER TABLE xproles ALTER COLUMN id SET NOT NULL;
ALTER TABLE xproles ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE xproles ALTER COLUMN required SET NOT NULL;
ALTER TABLE posroles ALTER COLUMN id SET NOT NULL;
ALTER TABLE posroles ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE posroles ALTER COLUMN max_members SET NOT NULL;
ALTER TABLE posrole_members ALTER COLUMN role_id SET NOT NULL;
ALTER TABLE posrole_members ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN channel_id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN author_id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN is_nsfw SET NOT NULL;
ALTER TABLE messages ALTER COLUMN forced_to SET NOT NULL;
ALTER TABLE messages ALTER COLUMN trashed SET NOT NULL;
ALTER TABLE messages ALTER COLUMN frozen SET NOT NULL;
ALTER TABLE sb_messages ALTER COLUMN message_id SET NOT NULL;
ALTER TABLE sb_messages ALTER COLUMN starboard_id SET NOT NULL;
ALTER TABLE sb_messages ALTER COLUMN last_known_star_count SET NOT NULL;
ALTER TABLE stars ALTER COLUMN message_id SET NOT NULL;
ALTER TABLE stars ALTER COLUMN starboard_id SET NOT NULL;
ALTER TABLE stars ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE _migrations ALTER COLUMN id_ SET NOT NULL;
CREATE INDEX _hash_index_aschannels__guild_id ON aschannels USING HASH ( ( guild_id ) );
CREATE INDEX _btree_index_guilds__premium_end ON guilds USING BTREE ( ( premium_end ) );
CREATE INDEX _hash_index_members__guild_id ON members USING HASH ( ( guild_id ) );
CREATE INDEX _hash_index_members__autoredeem_enabled ON members USING HASH ( ( autoredeem_enabled ) );
CREATE INDEX _btree_index_members__xp ON members USING BTREE ( ( xp ) );
CREATE UNIQUE INDEX _btree_index_overrides__guild_id_name ON overrides USING BTREE ( ( guild_id ) , ( name ) );
CREATE INDEX _hash_index_overrides__starboard_id ON overrides USING HASH ( ( starboard_id ) );
CREATE INDEX _gin_index_overrides__channel_ids ON overrides USING GIN ( ( channel_ids ) );
CREATE UNIQUE INDEX _btree_index_sb_messages__sb_message_id ON sb_messages USING BTREE ( ( sb_message_id ) );
CREATE INDEX _btree_index_sb_messages__last_known_star_count ON sb_messages USING BTREE ( ( last_known_star_count ) );
CREATE INDEX _hash_index_sb_messages__starboard_id ON sb_messages USING HASH ( ( starboard_id ) );
CREATE INDEX _hash_index_permroles__guild_id ON permroles USING HASH ( ( guild_id ) );
CREATE UNIQUE INDEX _btree_index_posroles__guild_id_max_members ON posroles USING BTREE ( ( guild_id ) , ( max_members ) );
CREATE INDEX _hash_index_starboards__guild_id ON starboards USING HASH ( ( guild_id ) );
CREATE INDEX _gin_index_starboards__star_emojis ON starboards USING GIN ( ( star_emojis ) );
CREATE INDEX _hash_index_xproles__guild_id ON xproles USING HASH ( ( guild_id ) );
CREATE INDEX _btree_index_stars__message_id_starboard_id ON stars USING BTREE ( ( message_id ) , ( starboard_id ) );
ALTER TABLE guilds ADD CONSTRAINT _guilds_id_primary_key PRIMARY KEY ( id );
ALTER TABLE users ADD CONSTRAINT _users_id_primary_key PRIMARY KEY ( id );
ALTER TABLE members ADD CONSTRAINT _members_user_id_guild_id_primary_key PRIMARY KEY ( user_id , guild_id );
ALTER TABLE starboards ADD CONSTRAINT _starboards_id_primary_key PRIMARY KEY ( id );
ALTER TABLE overrides ADD CONSTRAINT _overrides_id_primary_key PRIMARY KEY ( id );
ALTER TABLE permroles ADD CONSTRAINT _permroles_id_primary_key PRIMARY KEY ( id );
ALTER TABLE permrole_starboards ADD CONSTRAINT _permrole_starboards_permrole_id_starboard_id_primary_key PRIMARY KEY ( permrole_id , starboard_id );
ALTER TABLE aschannels ADD CONSTRAINT _aschannels_id_primary_key PRIMARY KEY ( id );
ALTER TABLE xproles ADD CONSTRAINT _xproles_id_primary_key PRIMARY KEY ( id );
ALTER TABLE posroles ADD CONSTRAINT _posroles_id_primary_key PRIMARY KEY ( id );
ALTER TABLE posrole_members ADD CONSTRAINT _posrole_members_role_id_user_id_primary_key PRIMARY KEY ( role_id , user_id );
ALTER TABLE messages ADD CONSTRAINT _messages_id_primary_key PRIMARY KEY ( id );
ALTER TABLE sb_messages ADD CONSTRAINT _sb_messages_message_id_starboard_id_primary_key PRIMARY KEY ( message_id , starboard_id );
ALTER TABLE stars ADD CONSTRAINT _stars_message_id_starboard_id_user_id_primary_key PRIMARY KEY ( message_id , starboard_id , user_id );
ALTER TABLE _migrations ADD CONSTRAINT __migrations_id__primary_key PRIMARY KEY ( id_ );
ALTER TABLE members ADD CONSTRAINT userid_fk FOREIGN KEY ( user_id ) REFERENCES users ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE members ADD CONSTRAINT guildid_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE starboards ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE overrides ADD CONSTRAINT guild_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE overrides ADD CONSTRAINT starboard_fk FOREIGN KEY ( starboard_id ) REFERENCES starboards ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE permroles ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE permrole_starboards ADD CONSTRAINT starboard_id_fk FOREIGN KEY ( starboard_id ) REFERENCES starboards ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE permrole_starboards ADD CONSTRAINT permrole_id_fk FOREIGN KEY ( permrole_id ) REFERENCES permroles ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE aschannels ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE xproles ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE posroles ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE posrole_members ADD CONSTRAINT role_id_fk FOREIGN KEY ( role_id ) REFERENCES posroles ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE posrole_members ADD CONSTRAINT user_id_fk FOREIGN KEY ( user_id ) REFERENCES users ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE messages ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE messages ADD CONSTRAINT author_id_fk FOREIGN KEY ( author_id ) REFERENCES users ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE sb_messages ADD CONSTRAINT message_id_fk FOREIGN KEY ( message_id ) REFERENCES messages ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE sb_messages ADD CONSTRAINT starboard_id_fk FOREIGN KEY ( starboard_id ) REFERENCES starboards ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE stars ADD CONSTRAINT message_id_fk FOREIGN KEY ( message_id ) REFERENCES messages ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE stars ADD CONSTRAINT starboard_id_fk FOREIGN KEY ( starboard_id ) REFERENCES starboards ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE stars ADD CONSTRAINT user_id_fk FOREIGN KEY ( user_id ) REFERENCES users ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;