#!/usr/bin/perl

# quota.cgi -- A simple perl-script for changing saslpasswords after authenticating on the imap-server.
# "Copyright (c) Oliver Pitzeier, June 2001"
#                 o.pitzeier@uptime.at
#
# This script was written for one of our customers.
# The rest? not interessting I think :-)
#
# Changes are welcome, but please inform me about those changes!
#
# Many thanks to Marcel Grünauer and Bernd Pinter who helped me to do the first steps in perl.

# Things we use in this script.
use strict;
use warnings;

use CGI qw/:standard/;
use IMAP::Admin;

my $version        = 1.2;

# Those lines are defining some values for the CGI-frontend.
my $passlen        = 12;
my $userlen        = 30;
my $overridefields = 1;

# Define some values for connection to the local imap-server.
my $imap_port      = 143;
my $imap_seperator = ".";
my $imap           = undef;

# Print some basic html-stuff.
    print header;
    print start_html(-title  =>'Change your password',
                     -author =>'o.pitzeier@uptime.at',
                     -BGCOLOR=>'#C3CACE'),"\n";

# Create a table and a form.
    print "<table border=0>\n";
    print start_form,"\n",
        "<tr><td>username: </td><td>",    textfield(     -name        =>'login',
                                                         -override    =>$overridefields,
                                                         -size        =>$userlen,
                                                         -maxlength   =>$userlen),"</td></tr>\n",
        "<tr><td>password: </td><td>",    password_field(-name        =>'password',
                                                         -override    =>$overridefields,
                                                         -size        =>$passlen,
                                                         -maxlength   =>$passlen),"</td></tr>\n";
    print "</table>\n";
    print submit(-value=>'send'),"\n";
    print end_form,"\n";
    print hr;
# End of the table and the form.    

# Check the parameters and do some error-catching.
# The stuff down here should be self-explaining.
# Don't forget to change the password for cyrus at line 72.
    if(param()) {
        if(param('login'))
        {
            if(param('password')) {
                $imap = IMAP::Admin->new('Server'    => 'localhost',
                                         'Login'     => param('login'),
                                         'Password'  => param('password'),
                                         'Port'      => $imap_port,
                                         'Separator' => $imap_seperator);
                if($imap->error eq 'No Errors') {
                    $imap->close;
                    $imap = IMAP::Admin->new('Server'    => 'localhost',
                                             'Login'     => "cyrus",
                                             'Password'  => "xxxxxxxxxxxxx",
                                             'Port'      => $imap_port,
                                             'Separator' => $imap_seperator);
                    my @quota = $imap->get_quota("user.".param('login'));
                    if(@quota) {
                        print "<table border=0>\n",
                              "<tr><td>Quota for:</td><td>".$quota[0]."</td></tr>\n",
                              "<tr><td>Used:</td><td>".$quota[1]."</td></tr>\n",
                              "<tr><td>Available:</td><td>".$quota[2]."</td></tr>\n",
                              "</table>\n";
                    } else {
                        print "Could not retrieve quota information";
                        print $imap->error;
                    }
                $imap->close;
                } else {
                    if($imap->error =~ /Login failed/) {
                        if($imap->error =~ /: authentication/) {
                            print "Wrong password! Could not log in.", br;
                        }
                        if($imap->error =~ /: user not found/) {
                            print "User not found! Could not log in.", br;
                        }
                    }
                }
            } else {
                print "No password given. Please enter your password!";
            }
        } else {
            print "No username given. Please enter your username!";
        }
    } else {
        print "Please enter the above informations!";
    }
    print hr,"\n",end_html;
