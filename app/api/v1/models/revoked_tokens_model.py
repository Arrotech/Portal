import json

from app.api.v1.models.database import Database

Database().create_table()


class RevokedToken(Database):
    """Initiallization."""

    def __init__(
            self,
            jti=None):
        super().__init__()
        self.jti = jti

    def save(self):
        """Add a new blacklisted token."""

        self.curr.execute(
            ''' INSERT INTO revoked_tokens(jti)\
            VALUES('{}')\
             RETURNING jti''' \
                .format(self.jti))
        revoked_token = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(revoked_token, default=str)

    def get_revoked_token(self, jti):
        """Get revoked token."""
        self.curr.execute(""" SELECT * FROM revoked_tokens WHERE jti=%s""", (jti,))
        revoked_token = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(revoked_token, default=str)
