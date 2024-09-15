from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from BillManagement.models import Bill, BillSplit
from BillManagement.serializers import BillSerializer, BillSplitSerializer

class BillCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id)
            bill_serializer = BillSerializer(bill)
            bill_splits = BillSplit.objects.filter(bill=bill)
            splits_serializer = BillSplitSerializer(bill_splits, many=True)
            response_data = {
                "bill": bill_serializer.data,
                "splits": splits_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Bill.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)


class BillUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id)
            serializer = BillSerializer(bill, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bill.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)


class BillDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id)
            bill.delete()
            return Response({"message": "Bill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Bill.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)


class BillSplitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id)
            splits_data = request.data.get('splits', [])
            for split_data in splits_data:
                split_data['bill'] = bill.id
                split_serializer = BillSplitSerializer(data=split_data)
                if split_serializer.is_valid():
                    split_serializer.save()
                else:
                    return Response(split_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Bill split successfully"}, status=status.HTTP_201_CREATED)
        except Bill.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)


class BillSplitUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, split_id):
        try:
            split = BillSplit.objects.get(id=split_id)
            serializer = BillSplitSerializer(split, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BillSplit.DoesNotExist:
            return Response({"message": "Bill Split not found"}, status=status.HTTP_404_NOT_FOUND)


class BillSplitDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, split_id):
        try:
            split = BillSplit.objects.get(id=split_id)
            split.delete()
            return Response({"message": "Bill Split deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except BillSplit.DoesNotExist:
            return Response({"message": "Bill Split not found"}, status=status.HTTP_404_NOT_FOUND)


class BillSettlementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, split_id):
        try:
            split = BillSplit.objects.get(id=split_id)
            split.status = "paid"
            split.save()
            return Response({"message": "Split settled successfully"}, status=status.HTTP_200_OK)
        except BillSplit.DoesNotExist:
            return Response({"message": "Split not found"}, status=status.HTTP_404_NOT_FOUND)
