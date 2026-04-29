/*
Copyright Perinet GmbH. All Rights Reserved.

This software is dual-licensed: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation. For the terms of this
license, see http://www.fsf.org/licensing/licenses/agpl-3.0.html,
or contact us at https://perinet.io/contact/ when you want license
this software under a commercial license.
*/

#pragma once

extern "C" {
#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wpedantic"
#endif  // __GNUC__
#include "cyclone_tcp/core/net.h"
#include "cyclone_tcp/http/http_server.h"
#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__


// #if (HTTP_SERVER_TLS_SUPPORT == ENABLED)
    error_t httpServerOpenSecureConnection(HttpServerContext *context, HttpConnection *connection);
    error_t httpServerEstablishSecureConnection(HttpConnection *connection);
    error_t httpServerUserCertificateCallback(TlsContext *tlsContext, const X509CertificateInfo *certInfo, uint_t pathLen, void *param);
// #endif
error_t httpServerShutdownConnection(HttpConnection *connection);
void httpServerCloseConnection(HttpConnection *connection);
error_t httpServerSendData(HttpConnection *connection, const void *data, size_t length, size_t *written, uint_t flags);
error_t httpServerReceiveData(HttpConnection *connection, void *data, size_t size, size_t *received, uint_t flags);
void httpServerChangeState(HttpConnection *connection, HttpConnState newState);
bool_t httpServerCheckTimeout(HttpConnection *connection, systime_t timeout);
}
