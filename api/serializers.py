from base_app.models import Referral, Guest
from auth_app.models import Contest, BusinessOwner
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)


class BusinessOwnerSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)
    contest = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='retrieve-user',
        read_only=True, lookup_field='pk'
    )

    class Meta:
        model = BusinessOwner
        fields = [
            'pk',
            "url",
            "username",
            "business_name",
            "phone_number",
            "full_name",
            "shortcode",
            'contest'
        ]
        read_only_fields = ['contest', 'shortcode']

    def get_contest(self, obj):
        return {
            "contests": obj.contests.values('id', 'cash_price', 'unique_id')
        }


class ContestSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)
    time = serializers.CharField(source='contest_time', read_only=True)
    past_time = serializers.CharField(source='past_contest_time', read_only=True)
    name = serializers.CharField(source='owner_name', read_only=True)
    business_owner_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source='owner_user', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="retrieve-contest", lookup_field="pk", read_only=True)
    business_owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contest
        fields = [
            'pk',
            "url",
            "name",
            "cash_price",
            "starting_date",
            "ending_date",
            "duration",
            "unique_id",
            "referral_count",
            "user",
            "business_owner",
            "time",
            "past_time",
            'business_owner_name'
        ]

    def get_business_owner_name(self, obj):
        print(obj, dir(obj))
        return {
            "Business Owner": obj.business_owner.business_name
        }

    def update(self, instance, validated_data):
        data = validated_data
        serializer = ContestSerializer(instance, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class ReferralSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)
    shortcode = serializers.CharField(source="ref_shortcode", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="referral", lookup_field="pk", read_only=True)
    referral_name = serializers.CharField(source="refer_name")
    contest = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = [
            "pk",
            "url",
            "referral_name",
            "business_owner",
            "phone_number",
            "shortcode",
            "contest"
        ]

    def get_contest(self, obj):
        return {
            "contest_id": obj.business_owner.id,
            "business_owner": obj.business_owner.business_owner.business_name
        }


class GuestSerializer(serializers.ModelSerializer):
    pk = serializers.IPAddressField(read_only=True)
    ip = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="retrieve-guest", lookup_field="pk")

    class Meta:
        model = Guest
        fields = [
            "pk",
            "url",
            # "referral",
            "business_owner",
            "ip",
            "guest_name",
            "phone_number",
        ]

    # def get_contest(self, obj):
    #     return {
    #         "contest": obj.business_owner.id,
    #         "referral": obj.referral.refer_name
    #     }

class VoteSerializer(serializers.ModelSerializer):
    # pk = serializers.CharField(read_only=True)
    guest_name = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = Guest
        fields = [
            "referral",
            "business_owner",
            "guest_name",
            "phone_number"
        ]
