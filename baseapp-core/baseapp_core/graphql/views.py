import json, logging

from django.http.response import HttpResponseBadRequest
from graphene_django.views import GraphQLView as GrapheneGraphQLView
from graphene_django.views import HttpError
from graphql import get_operation_ast, parse
from graphql.execution import ExecutionResult
from graphene_file_upload.utils import place_files_in_operations

try:
    import sentry_sdk
except ModuleNotFoundError:
    sentry_sdk = None


class GraphQLView(GrapheneGraphQLView):
    def execute_graphql_request(
        self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        if not query:
            if show_graphiql:
                return None
            raise HttpError(HttpResponseBadRequest("Must provide query string."))

        if sentry_sdk:
            if sentry_sdk.Hub.current.scope.transaction:
                try:
                    document = parse(query)
                except Exception as e:
                    return ExecutionResult(errors=[e])

                operation_ast = get_operation_ast(document, operation_name)
                operation_type = operation_ast.operation.value

                if operation_name:
                    sentry_sdk.Hub.current.scope.transaction.name = operation_name
                if operation_type:
                    sentry_sdk.Hub.current.scope.transaction.op = operation_type

        return super().execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )


    def parse_body(self, request):
        """Handle multipart request spec for multipart/form-data"""
        content_type = self.get_content_type(request)
        # logging.info('content_type: %s' % content_type)
        # import pdb; pdb.set_trace()
        if content_type == 'multipart/form-data' and 'operations' in request.POST:
            operations = json.loads(request.POST.get('operations', '{}'))
            # import pdb; pdb.set_trace()
            files_map = json.loads(request.POST.get('map', '{}'))
            return place_files_in_operations(
                operations,
                files_map,
                request.FILES
            )
        return super(GraphQLView, self).parse_body(request)
