/* GStreamer
 * Copyright (C) 2008 Wim Taymans <wim.taymans at gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

// vlc rtsp://beaglebone.iemnet:8554/test
 
#include <gst/gst.h>
 
#include <gst/rtsp-server/rtsp-server.h>

#include <string.h>
#define URILEN 1024
 
/* define this if you want the resource to only be available when using
 * user/admin as the password */
#undef WITH_AUTH

/* an idle function that gets called periodically */
#include <sys/time.h>

/* this timeout is periodically run to clean up the expired sessions from the
 * pool. This needs to be run explicitly currently but might be done
 * automatically as part of the mainloop. */

static gboolean
timeout (GstRTSPServer * server, gboolean ignored)
{
  GstRTSPSessionPool *pool;
 
  pool = gst_rtsp_server_get_session_pool (server);
  gst_rtsp_session_pool_cleanup (pool);
  g_object_unref (pool);
 
  return TRUE;
}
 
int
main (int argc, char *argv[])
{
  GMainLoop *loop;
  GstRTSPServer *server;
  GstRTSPMediaMapping *mapping;
  GstRTSPMediaFactory *factory;
#ifdef WITH_AUTH
  GstRTSPAuth *auth;
  gchar *basic;
#endif
  const char*mountpoint="/MINT";
  guint serverID=0;
  guint port=8554;
  const char*pipeline =
    "audiotestsrc ! "
    "audioconvert ! "
    "audio/x-raw-int,channels=4 ! "
    "rtpL16pay name=pay0"
    ;
  const char*outfile=NULL;
  char URI[URILEN];

  gst_init (&argc, &argv);

  argc--; argv++;
#define NONEMPTY_ARG(x)   \
    do {                  \
      if(argc-->0) {      \
        char*arg=*argv++; \
        if(strlen(arg)>0) \
          x=arg;          \
    } } while(0)
  NONEMPTY_ARG(pipeline);
  NONEMPTY_ARG(mountpoint);
  NONEMPTY_ARG(outfile);

  loop = g_main_loop_new (NULL, FALSE);
 
  /* create a server instance */
  server = gst_rtsp_server_new ();
 
  /* get the mapping for this server, every server has a default mapper object
   * that be used to map uri mount points to media factories */
  mapping = gst_rtsp_server_get_media_mapping (server);
 
#ifdef WITH_AUTH
  /* make a new authentication manager. it can be added to control access to all
   * the factories on the server or on individual factories. */
  auth = gst_rtsp_auth_new ();
  basic = gst_rtsp_auth_make_basic ("user", "admin");
  gst_rtsp_auth_set_basic (auth, basic);
  g_free (basic);
  /* configure in the server */
  gst_rtsp_server_set_auth (server, auth);
#endif
 
  /* make a media factory for a test stream. The default media factory can use
   * gst-launch syntax to create pipelines.
   * any launch line works as long as it contains elements named pay%d. Each
   * element with pay%d names will be a stream */
  factory = gst_rtsp_media_factory_new ();

  gst_rtsp_media_factory_set_launch (factory,
				     pipeline
				     );
 
  /* attach the test factory to the /test url */
  gst_rtsp_media_mapping_add_factory (mapping, mountpoint, factory);
 
  /* don't need the ref to the mapper anymore */
  g_object_unref (mapping);
 
  /* attach the server to the default maincontext */
  while(!serverID) {
    char portS[6];
    portS[5]=0;
    snprintf(portS, 6, "%d", port);
    gst_rtsp_server_set_service(server, portS);
    serverID=gst_rtsp_server_attach (server, NULL);
    if(port>=65530)
      goto failed;
    port++;
  }
 
  /* add a timeout for the session cleanup */
  g_timeout_add_seconds (2, (GSourceFunc) timeout, server);

  snprintf(URI, URILEN, "rtsp://@HOSTNAME@:%s%s", gst_rtsp_server_get_service(server), mountpoint);
  if(outfile) {
    FILE*f=fopen(outfile, "w");
    if(f) {
      fprintf(f, "%s\n", URI);
      fflush(f);
      fclose(f);
    }
  } else {
    printf("%s\n", URI);
    fflush(stdout);fflush(stderr);
  }

  g_warning ("%s\n", URI);

  /* start serving, this never stops */
  g_main_loop_run (loop);
 
  return 0;
 
  /* ERRORS */
failed:
  {
    g_warning ("failed to attach the server");
    return -1;
  }
}
