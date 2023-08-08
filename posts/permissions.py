from rest_framework.permissions import BasePermission

from rest_framework import permissions

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.user:
                return True
            else:
                return False
        else:
            return False
        


# Post 작성자에 한해 수정 / 삭제 권한을 부여
class IsAuthorOrReadonly(permissions.BasePermission):
    
    # 인증된 유저에 대해 목록 조회 / 포스팅 등록 허용
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    # 작성자에 한에 Record에 대한 수정 / 삭제 허용
    def has_object_permission(self, request, view, obj):
        # 조회 요청은 항상 True
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT, DELETE 요청에 한해, 작성자에게만 허용
        return obj.writer == request.user
    

# Post 작성자에 한해 수정 권한은 부여하되 삭제 권한은 superuser에게만 부여
class IsAuthorUpdateOrReadOnly(permissions.BasePermission):
    def has_permission(slef, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if (request.method == 'DELETE'):
            return request.user.is_superuser
        
        return obj.writer == request.user
