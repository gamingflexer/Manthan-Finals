import json
import time
import subprocess

from lib.cmd import Parser
from hookers.weleakinfo_hook import WeLeakInfoHook
from hookers.hunter_io_hook import HunterIoHook
from hookers.hibp_hook import BeenPwnedHook
from hookers.dehashed_hook import DehashedHook
from hookers.databasestoday_hook import DatabasesTodayHook
from hookers.emailrep_io_hook import EmailRepHook
from hookers.snusbase_hooker import SnusbaseHooker
from lib.settings import (
    test_file,
    BANNER,
    display_found_databases,
    grab_api_tokens,
    check_ten_minute_email,
    TEN_MINUTE_EMAIL_EXTENSION_LIST
)
from lib.formatter import (
    info,
    error,
    warn,
    prompt
)


def main():
    try:
        opt = Parser().optparse()
        print(BANNER)
        res = Parser().check_opts(opt)
        if res is not None:
            to_search = res
        else:
            to_search = []
        do_not_search = []

        if len(to_search) == 0:
            if opt.singleEmail is None and opt.emailFile is None:
                warn("you have not provided an email to scan, redirecting to the help menu")
                subprocess.call(["python", "whatbreach.py", "--help"])
                exit(1)
            api_tokens = grab_api_tokens()
            if opt.searchHunterIo and opt.singleEmail is not None:
                info("starting search on hunter.io using {}".format(opt.singleEmail))
                file_results = HunterIoHook(
                    opt.singleEmail, api_tokens["hunter.io"], verify_emails=opt.verifyEmailsThroughHunterIo
                ).hooker()
                if file_results is not None:
                    with open(file_results) as data:
                        emails = json.loads(data.read())["discovered_emails"]
                    for email in emails:
                        to_search.append(email)
                else:
                    to_search.append(opt.singleEmail)
            elif opt.searchHunterIo and opt.emailFile is not None:
                if not test_file(opt.emailFile):
                    error("unable to open filename, does it exist?")
                    exit(1)
                api_tokens = grab_api_tokens()
                with open(opt.emailFile) as data:
                    for email in data.readlines():
                        email = email.strip()
                        file_results = HunterIoHook(
                            email, api_tokens["hunter.io"], verify_emails=opt.verifyEmailsThroughHunterIo
                        ).hooker()
                        with open(file_results) as results:
                            discovered_emails = json.loads(results.read())["discovered_emails"]
                        for discovered in discovered_emails:
                            to_search.append(discovered)
            elif opt.singleEmail is not None:
                info("starting search on single email address: {}".format(opt.singleEmail))
                to_search = [opt.singleEmail]
            elif opt.emailFile is not None:
                if not test_file(opt.emailFile):
                    error("unable to open filename, does it exist?")
                    exit(1)
                with open(opt.emailFile) as emails:
                    info("parsing email file: {}".format(opt.emailFile))
                    to_search = emails.readlines()
                info("starting search on a total of {} email(s)".format(len(to_search)))

        for email in to_search:
            email = email.strip()

            if opt.checkTenMinuteEmail:
                if check_ten_minute_email(email, TEN_MINUTE_EMAIL_EXTENSION_LIST):
                    warn("email: {} appears to be a ten minute email".format(email))
                    answer = prompt("would you like to process the email[y/N]")
                    if answer.startswith("n"):
                        do_not_search.append(email)

            if opt.checkEmailAccounts:
                info("searching for possible profiles related to {}".format(email))
                searcher = EmailRepHook(email)
                results = searcher.hooker()
                if results is not None and len(results) != 0:
                    info(
                        "found a total of {} possible profiles associated with {} on the following domains:".format(
                            len(results), email
                        )
                    )
                    for domain in results:
                        print("\t-> {}".format(domain.title()))
                else:
                    warn("no possible profiles discovered for email: {}".format(email))

            if email not in do_not_search:
                if opt.throttleRequests != 0:
                    time.sleep(opt.throttleRequests)
                info("searching breached accounts on HIBP related to: {}".format(email))
                account_dumps = BeenPwnedHook(
                    email, api_tokens["haveibeenpwned.com"], opt, retry=opt.retryOnFail
                ).account_hooker()
                info("searching for paste dumps on HIBP related to: {}".format(email))

                if opt.searchPastebin:
                    paste_dumps = BeenPwnedHook(
                        email, api_tokens["haveibeenpwned.com"], opt, retry=opt.retryOnFail
                    ).paste_hooker()
                else:
                    warn("suppressing discovered pastes")
                    paste_dumps = []

                if opt.searchWeLeakInfo:
                    info("searching weleakinfo.com for breaches related to: {}".format(email))
                    searcher = WeLeakInfoHook(email, api_tokens["weleakinfo.com"])
                    tmp = set()
                    results = searcher.hooker()
                    if results is not None:
                        if account_dumps is not None:
                            original_length = len(account_dumps)
                        else:
                            original_length = 0
                        if account_dumps is not None:
                            for item in account_dumps:
                                tmp.add(item)
                        if results is not None:
                            for item in results:
                                tmp.add(item)
                        if len(tmp) != 0:
                            account_dumps = list(tmp)
                            new_length = len(account_dumps)
                            amount_discovered = new_length - original_length
                            if amount_discovered != 0:
                                info(
                                    "discovered a total of {} more breaches from weleakinfo.com".format(
                                        new_length - original_length
                                    )
                                )
                            else:
                                warn("did not discover any breaches")
                        else:
                            warn("did not discover any new databases from weleakinfo.com")
                    else:
                        warn("no databases discovered on weleakinfo")

                if opt.searchSnusBase:
                    info("searching snusbase.com for breaches related to '{}'".format(email))
                    snusbase_leaks = SnusbaseHooker(
                        email, api_tokens["snusbase.com"]["username"],
                        api_tokens["snusbase.com"]["password"]
                    ).main()
                    if snusbase_leaks is not None and len(snusbase_leaks) != 0:
                        info("found a total of {} more leaks using snusbase".format(len(snusbase_leaks)))
                        for item in snusbase_leaks:
                            account_dumps.append(item)
                            set(account_dumps)
                            account_dumps = list(account_dumps)
                    else:
                        warn("did not find anymore leaks using snusbase")

                if account_dumps is not None and paste_dumps is not None and len(account_dumps) != 0:
                    info(
                        "found a total of {} database breach(es) and a total of {} paste(s) pertaining to: {}".format(
                            len(account_dumps), len(paste_dumps), email
                        )
                    )
                    if opt.searchDehashed:
                        if len(account_dumps) > 20:
                            warn(
                                "large amount of database breaches, obtaining links from "
                                "dehashed (this may take a minute)"
                            )
                        found_databases = DehashedHook(account_dumps).hooker()
                    else:
                        warn("suppressing discovered databases")
                        found_databases = {}
                    for i, dump in enumerate(paste_dumps, start=1):
                        found_databases["Paste#{}".format(i)] = str(dump)
                    display_found_databases(found_databases, download_pastes=opt.downloadPastes)
                    if opt.downloadDatabase:
                        for item in found_databases.keys():
                            if "Paste" not in item:
                                info("searching for downloadable databases using query: {}".format(item.lower()))
                                downloaded = DatabasesTodayHook(
                                    str(item), downloads_directory=opt.saveDirectory
                                ).hooker()
                                if len(downloaded) != 0:
                                    info(
                                        "downloaded a total of {} database(s) pertaining to query: {}".format(
                                            len(downloaded), item
                                        )
                                    )
                                    display_found_databases(
                                        downloaded, is_downloaded=True, download_pastes=opt.downloadPastes
                                    )
                                else:
                                    warn(
                                        "no databases appeared to be present and downloadable related to query: {}".format(
                                            str(item)
                                        )
                                    )

                elif account_dumps is not None and paste_dumps is None and len(account_dumps) != 0:
                    info("found a total of {} database breach(es) pertaining to: {}".format(len(account_dumps), email))
                    if opt.searchDehashed:
                        if len(account_dumps) > 20:
                            warn(
                                "large amount of database breaches, obtaining links from "
                                "dehashed (this may take a minute)"
                            )
                        found_databases = DehashedHook(account_dumps).hooker()
                    else:
                        warn("suppressing discovered databases")
                        found_databases = {}
                    if len(found_databases) != 0:
                        display_found_databases(found_databases, download_pastes=opt.downloadPastes)
                        if opt.downloadDatabase:
                            for item in found_databases.keys():
                                if "Paste" not in item:
                                    info("searching for downloadable databases using query: {}".format(item.lower()))
                                    downloaded = DatabasesTodayHook(
                                        str(item), downloads_directory=opt.saveDirectory
                                    ).hooker()
                                    if len(downloaded) != 0:
                                        info(
                                            "downloaded a total of {} database(s) pertaining to query: {}".format(
                                                len(downloaded), item
                                            )
                                        )
                                        display_found_databases(
                                            downloaded, is_downloaded=True, download_pastes=opt.downloadPastes
                                        )
                                    else:
                                        warn(
                                            "no databases appeared to be present and downloadable related to query: {}".format(
                                                str(item)
                                            )
                                        )
                    else:
                        warn("no output to show, most likely due to output suppression or dehashed")
                elif account_dumps is None and paste_dumps is not None:
                    # this should never happen
                    error("no database dumps found nor any pastes found for: {}".format(email))
                else:
                    error("email {} was not found in any breach".format(email))

        if opt.staySalty:
            # i know that you think that you know shit
            # all the shade that's coming at me I wonder who throws it
            # you can't see the vision boy, you must be outta focus
            # that's a real hot program homie, I wonder who wrote it? oh shit
            # (lyrics ripped from iSpy by Kyle, all I do is steal bruh)
            warn("all this code was stolen with <3 by Eku")
    except KeyboardInterrupt:
        error("user quit the session")