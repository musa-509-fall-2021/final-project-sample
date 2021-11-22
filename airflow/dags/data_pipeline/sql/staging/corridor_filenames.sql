-- Each corridor will have it's own report file. This transformation strips out
-- a bunch of the cruft characters from the corridor name to arrive at something
-- that is appropriate to be used as a file name.
--
-- Gets rid of: ".", "/"
-- Replaces spaces and ampersands with "-"

SELECT
    corridorkey,
    LOWER(
        REPLACE(
        REPLACE(
        REPLACE(
        REPLACE(
        REPLACE(
        REPLACE(
            name,
            '.'  , '' ),
            ' / ', '' ),
            '/'  , '' ),
            ' - ', ' '),
            ' & ', ' '),
            ' '  , '-')
        ) as filename,
FROM staging.corridor_base
