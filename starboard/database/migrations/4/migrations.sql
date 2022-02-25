CREATE TABLE permrole_starboards ();
CREATE TABLE permroles ();
ALTER TABLE permrole_starboards ADD COLUMN permrole_id NUMERIC;
ALTER TABLE permrole_starboards ADD COLUMN starboard_id NUMERIC;
ALTER TABLE permrole_starboards ADD COLUMN give_stars BOOLEAN;
ALTER TABLE permrole_starboards ADD COLUMN recv_stars BOOLEAN;
ALTER TABLE permroles ADD COLUMN id NUMERIC;
ALTER TABLE permroles ADD COLUMN guild_id NUMERIC;
ALTER TABLE permroles ADD COLUMN xproles BOOLEAN;
ALTER TABLE permroles ADD COLUMN give_stars BOOLEAN;
ALTER TABLE permroles ADD COLUMN recv_stars BOOLEAN;
ALTER TABLE permrole_starboards ALTER COLUMN permrole_id SET NOT NULL;
ALTER TABLE permrole_starboards ALTER COLUMN starboard_id SET NOT NULL;
ALTER TABLE permroles ALTER COLUMN id SET NOT NULL;
ALTER TABLE permroles ALTER COLUMN guild_id SET NOT NULL;
ALTER TABLE permrole_starboards ADD CONSTRAINT _permrole_starboards_permrole_id_starboard_id_primary_key PRIMARY KEY ( permrole_id , starboard_id );
ALTER TABLE permroles ADD CONSTRAINT _permroles_id_primary_key PRIMARY KEY ( id );
ALTER TABLE permrole_starboards ADD CONSTRAINT starboard_id_fk FOREIGN KEY ( starboard_id ) REFERENCES starboards ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE permroles ADD CONSTRAINT guild_id_fk FOREIGN KEY ( guild_id ) REFERENCES guilds ( id ) MATCH SIMPLE ON DELETE CASCADE ON UPDATE CASCADE;