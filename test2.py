import datetime
from handy import str2date, date2str


s = '2023-01-02'



print(f'{s} --> {isoform2dmY(s)} --> {dmY2isoform(isoform2dmY(s))}')