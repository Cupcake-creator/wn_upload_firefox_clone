from sre_constants import SUCCESS
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import UploadForm
from .models import Upload
import os
from django.utils import timezone

# TODO:
    # 1) Convert expire_duration to expire_date ✔️
    # 2) Upload and save ✔️
    # 3) Generate download and delete link ✔️ (<a> tag)
    # 4) limit file size ✔️ (in model)
class UploadPage(LoginRequiredMixin, CreateView):
    form_class = UploadForm
    model = Upload
    login_url = '/login/'
    redirect_field_name = 'login'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        form = self.get_form()
        if form.is_valid():
            uploaded = form.save()
            uploaded.user = request.user
            uploaded.save()
            return HttpResponse(f"<a href='/'>Back to upload page</a><br/><a href='/{uploaded.id}'>Download Link</a><br/><a href='delete/{uploaded.id}'>Delete Link</a>") 
        else:
            return self.form_invalid(form)


# TODO:
    # Make it so that you can't download expired files ✔️ (in get() method)
    # 1) Delete file when max_downloads is done ✔️ 
    # 2) Verify password securely ✔️
    # 3) Actually send the download ✔️
class Download(DetailView):
    model = Upload

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        path = self.object.file.name
        if self.object.max_downloads > 0 and self.object.expire_date > timezone.now():
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            self.object.delete()
            os.remove(path)
            raise Http404("Expried data or Deleted data.")

    # check password is available and check password is correct
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.password is not None:
            if  not self.object.verify_password(self.request.POST.get("password")):
                return HttpResponse("invalid password")

        # read file and send request
        with open(self.object.file.name, 'rb') as fh:
            path = self.object.file.name
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + path.split('/')[-1]
            self.object.max_downloads -= 1
            self.object.save()
            fh.close()
            if self.object.max_downloads <= 0 :
                self.object.delete()
                os.remove(path)
            return response
        

# TODO: Actually delete fil ✔️
class Delete(LoginRequiredMixin,DetailView):
    model = Upload
    template_name = "upload/delete.html"
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        path = self.object.file.name
        if self.object.max_downloads > 0 and self.object.expire_date > timezone.now():
            if self.object.user == request.user:
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            return HttpResponse("<h1 style='color:red;'>You have no permission to delete this object.</h1>")
        else:
            self.object.delete()
            os.remove(path)
            raise Http404("Expried data or Deleted data.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        path = self.object.file.name
        self.object.delete()
        os.remove(path)
        return HttpResponse("Deleted!")

