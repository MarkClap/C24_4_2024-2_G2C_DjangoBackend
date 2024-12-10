# views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users, Roles, UserRoles
from .serializers import UserSerializer


class AssignRoleView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        users = Users.objects.all()

        user_serializer = UserSerializer(users, many=True)
        
        roles = Roles.objects.all()

        users_with_roles = [
            {
                "user": user,
                "roles": UserRoles.objects.filter(user=user).select_related('role')
            }
            for user in users
        ]
        
        role_data = [{'id': role.id, 'name': role.name} for role in roles]

        return Response({
            'users': user_serializer.data,
            'roles': role_data, 
        })

    def post(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        if not user_id or not role_id:
            return Response({'detail': 'User ID and Role ID are required'}, status=400)

        try:
            user = Users.objects.get(id=user_id)
            role = Roles.objects.get(id=role_id)

            user_role, created = UserRoles.objects.get_or_create(user=user, role=role)

            if created:
                return Response({'message': f"Role '{role.name}' assigned to user '{user.username}' successfully!"})
            else:
                return Response({'message': f"User '{user.username}' already has the role '{role.name}'."})

        except Users.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)
        except Roles.DoesNotExist:
            return Response({'detail': 'Role not found'}, status=404)

class RemoveRoleView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = Users.objects.all()
        
        user_serializer = UserSerializer(users, many=True)
        
        roles = Roles.objects.all()
        
        users_with_roles = [
            {
                "user": user,
                "roles": UserRoles.objects.filter(user=user).select_related('role')
            }
            for user in users
        ]
        
        role_data = [{'id': role.id, 'name': role.name} for role in roles]

        return Response({
            'users': user_serializer.data,
            'roles': role_data,  
        })

    def delete(self, request):
        user_id = request.data.get('user_id') 
        role_id = request.data.get('role_id')  

        if not user_id or not role_id:
            return Response({'detail': 'User ID and Role ID are required'}, status=400)

        try:
            user = Users.objects.get(id=user_id)
            role = Roles.objects.get(id=role_id)

            user_role = UserRoles.objects.get(user=user, role=role)
            user_role.delete() 

            users = Users.objects.all()
            user_serializer = UserSerializer(users, many=True)
            roles = Roles.objects.all()
            role_data = [{'id': role.id, 'name': role.name} for role in roles]

            return Response({
                'message': f"Role '{role.name}' removed from user '{user.username}' successfully!",
                'users': user_serializer.data,
                'roles': role_data,
            })

        except Users.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)
        except Roles.DoesNotExist:
            return Response({'detail': 'Role not found'}, status=404)
        except UserRoles.DoesNotExist:
            return Response({'detail': 'Role not assigned to user'}, status=404)